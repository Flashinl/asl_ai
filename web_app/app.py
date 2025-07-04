"""
Main Flask web application for ASL-to-Text AI system.
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import base64
import io
from PIL import Image
import threading
import time

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from translation.asl_translator import ASLTranslator
from utils.config import get_config, validate_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asl-ai-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file upload

# Enable CORS
CORS(app, origins=["*"])

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global translator instance
translator = None
config = get_config()

def initialize_translator():
    """Initialize the ASL translator with default models."""
    global translator
    try:
        # For now, initialize without pre-trained models
        # In production, you would load actual trained models
        translator = ASLTranslator()
        logger.info("ASL Translator initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize translator: {e}")
        return False

@app.route('/')
def index():
    """Main landing page."""
    return render_template('index.html')

@app.route('/live')
def live_translation():
    """Live video translation page."""
    return render_template('live_translation.html')

@app.route('/upload')
def upload_translation():
    """File upload translation page."""
    return render_template('upload_translation.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "translator_ready": translator is not None,
        "version": "1.0.0"
    })

@app.route('/api/translate/upload', methods=['POST'])
def translate_uploaded_video():
    """
    Translate an uploaded video file.
    """
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No video file selected"}), 400
    
    if not translator:
        return jsonify({"error": "Translator not initialized"}), 500
    
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{video_file.filename}"
        video_file.save(temp_path)
        
        # Process video
        frames = extract_frames_from_video(temp_path)
        
        if not frames:
            return jsonify({"error": "Could not extract frames from video"}), 400
        
        # Translate video
        result = translator.translate_video_sequence(frames)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "translation": result["final_text"],
            "word_count": len(result["words"]),
            "processing_stats": result["processing_stats"],
            "confidence_scores": [w["confidence"] for w in result["words"]]
        })
        
    except Exception as e:
        logger.error(f"Video translation failed: {e}")
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

def extract_frames_from_video(video_path: str, max_frames: int = 1000):
    """
    Extract frames from a video file.
    
    Args:
        video_path: Path to video file
        max_frames: Maximum number of frames to extract
        
    Returns:
        List of video frames as numpy arrays
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        logger.error(f"Could not open video file: {video_path}")
        return frames
    
    frame_count = 0
    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize frame for processing
        frame = cv2.resize(frame, (640, 480))
        frames.append(frame)
        frame_count += 1
    
    cap.release()
    logger.info(f"Extracted {len(frames)} frames from video")
    return frames

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {request.sid}")
    emit('status', {'message': 'Connected to ASL translator'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('start_translation')
def handle_start_translation():
    """Start real-time translation session."""
    if not translator:
        emit('error', {'message': 'Translator not initialized'})
        return
    
    # Reset translator state for new session
    translator.reset_translation_state()
    emit('translation_started', {'message': 'Translation session started'})
    logger.info(f"Translation session started for client: {request.sid}")

@socketio.on('video_frame')
def handle_video_frame(data):
    """
    Handle incoming video frame for real-time translation.
    
    Args:
        data: Dictionary containing base64 encoded frame data
    """
    if not translator:
        emit('error', {'message': 'Translator not initialized'})
        return
    
    try:
        # Decode base64 frame
        frame_data = data['frame'].split(',')[1]  # Remove data:image/jpeg;base64,
        frame_bytes = base64.b64decode(frame_data)
        
        # Convert to OpenCV format
        image = Image.open(io.BytesIO(frame_bytes))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Process frame
        timestamp = time.time()
        result = translator.translate_frame(frame, timestamp)
        
        # Send results back to client
        response = {
            'timestamp': timestamp,
            'processing_time': result['processing_time'],
            'buffer_size': result['buffer_size'],
            'detection_ready': result['detection_ready']
        }
        
        # If a word was detected, send it
        if result['word_added']:
            response.update({
                'word': result['text'],
                'confidence': result['confidence'],
                'sentence_complete': result['sentence_complete']
            })
            
            # If sentence is complete, send processed sentence
            if result['sentence_complete'] and 'processed_sentence' in result:
                response['processed_sentence'] = result['processed_sentence']
        
        # Send current sentence being built
        current_sentence = translator.get_current_sentence()
        if current_sentence:
            response['current_sentence'] = current_sentence
        
        emit('translation_result', response)
        
    except Exception as e:
        logger.error(f"Frame processing failed: {e}")
        emit('error', {'message': f'Frame processing failed: {str(e)}'})

@socketio.on('stop_translation')
def handle_stop_translation():
    """Stop real-time translation session."""
    if translator:
        # Get final sentence
        final_sentence = translator.get_current_sentence()
        stats = translator.get_translation_stats()
        
        emit('translation_stopped', {
            'final_sentence': final_sentence,
            'stats': stats
        })
        
        # Reset translator state
        translator.reset_translation_state()
    
    logger.info(f"Translation session stopped for client: {request.sid}")

@app.route('/api/stats')
def get_translation_stats():
    """Get current translation statistics."""
    if not translator:
        return jsonify({"error": "Translator not initialized"}), 500
    
    stats = translator.get_translation_stats()
    return jsonify(stats)

@app.route('/api/vocabulary')
def get_vocabulary_info():
    """Get vocabulary information."""
    if not translator:
        return jsonify({"error": "Translator not initialized"}), 500
    
    vocab_stats = translator.vocabulary.get_vocabulary_stats()
    return jsonify(vocab_stats)

@app.route('/api/vocabulary/categories')
def get_vocabulary_categories():
    """Get vocabulary categories."""
    if not translator:
        return jsonify({"error": "Translator not initialized"}), 500
    
    categories = translator.vocabulary.get_categories()
    return jsonify({"categories": categories})

@app.route('/api/vocabulary/category/<category>')
def get_words_by_category(category):
    """Get words in a specific category."""
    if not translator:
        return jsonify({"error": "Translator not initialized"}), 500
    
    words = translator.vocabulary.get_words_by_category(category)
    return jsonify({"category": category, "words": words})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

def main():
    """Main application entry point."""
    # Validate configuration
    if not validate_config():
        logger.error("Configuration validation failed")
        return
    
    # Initialize translator
    if not initialize_translator():
        logger.error("Failed to initialize translator")
        return
    
    # Get configuration
    web_config = config['web']
    
    logger.info("Starting ASL-to-Text AI web application")
    logger.info(f"Server will run on {web_config['host']}:{web_config['port']}")
    
    # Run the application
    socketio.run(
        app,
        host=web_config['host'],
        port=web_config['port'],
        debug=web_config['debug'],
        allow_unsafe_werkzeug=True
    )

if __name__ == '__main__':
    main()
