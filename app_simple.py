"""
Simplified ASL-to-Text AI app for Render deployment.
This version provides the web interface without heavy ML dependencies.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
           template_folder='web_app/templates',
           static_folder='web_app/static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asl-ai-demo-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

# Enable CORS
CORS(app, origins=["*"])

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
    """File upload translation page (demo mode)."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Translation - ASL-to-Text AI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Video Upload Translation</h1>
            <div class="alert alert-info">
                <h4>Demo Mode</h4>
                <p>This is a demonstration version. The full AI translation capabilities require additional ML dependencies.</p>
                <p>For the complete system with real-time ASL translation, please see the local installation instructions.</p>
            </div>
            <a href="/" class="btn btn-primary">Back to Home</a>
        </div>
    </body>
    </html>
    """

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0-demo",
        "mode": "demo",
        "message": "ASL-to-Text AI Demo - Full ML features require local installation"
    })

@app.route('/api/demo')
def demo_info():
    """Demo information endpoint."""
    return jsonify({
        "demo_mode": True,
        "features": {
            "web_interface": "✅ Available",
            "real_time_translation": "⚠️ Requires local installation",
            "video_upload": "⚠️ Requires local installation",
            "ml_models": "⚠️ Requires local installation"
        },
        "instructions": {
            "local_setup": "git clone https://github.com/Flashinl/asl_ai.git && pip install -r requirements.txt",
            "run_locally": "python web_app/app.py"
        }
    })

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
    # Use Render's PORT environment variable if available
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    logger.info("Starting ASL-to-Text AI Demo Web Application")
    logger.info(f"Server will run on {host}:{port}")
    logger.info("Demo mode - Full ML features require local installation")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main()
