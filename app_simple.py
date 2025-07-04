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

# Initialize Flask app with absolute paths
import os
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / 'web_app' / 'templates'
STATIC_DIR = BASE_DIR / 'web_app' / 'static'

app = Flask(__name__,
           template_folder=str(TEMPLATE_DIR),
           static_folder=str(STATIC_DIR))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asl-ai-demo-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

# Enable CORS
CORS(app, origins=["*"])

@app.route('/')
def index():
    """Main landing page."""
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback if template not found
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ASL-to-Text AI</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1>🤟 ASL-to-Text AI</h1>
                <p class="lead">Advanced AI system for translating American Sign Language into written text.</p>
                <div class="alert alert-info">
                    <h4>Demo Mode</h4>
                    <p>This is a demonstration version running on Render.</p>
                    <p>Template error: {str(e)}</p>
                </div>
                <div class="row mt-4">
                    <div class="col-md-6">
                        <h3>Features</h3>
                        <ul>
                            <li>Real-time ASL translation</li>
                            <li>Video file upload support</li>
                            <li>Advanced AI models</li>
                            <li>Professional web interface</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h3>Quick Links</h3>
                        <a href="/api/health" class="btn btn-primary">Health Check</a>
                        <a href="/api/demo" class="btn btn-info">Demo Info</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

@app.route('/live')
def live_translation():
    """Live video translation page (demo mode)."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live ASL Translation - ASL-to-Text AI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            .video-placeholder {
                background: #000;
                border-radius: 10px;
                height: 300px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.2rem;
            }
            .demo-alert {
                border-left: 4px solid #17a2b8;
                background: #d1ecf1;
                padding: 20px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="fas fa-hands"></i> ASL-to-Text AI
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">Home</a>
                    <a class="nav-link active" href="/live">Live Translation</a>
                    <a class="nav-link" href="/upload">Upload Video</a>
                </div>
            </div>
        </nav>

        <div class="container-fluid py-4">
            <div class="demo-alert">
                <h4><i class="fas fa-info-circle"></i> Demo Mode</h4>
                <p><strong>This is a demonstration version.</strong> The live translation feature requires the full AI system with computer vision capabilities.</p>
                <p>To experience real-time ASL translation:</p>
                <ol>
                    <li>Clone the repository: <code>git clone https://github.com/Flashinl/asl_ai.git</code></li>
                    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                    <li>Run locally: <code>python web_app/app.py</code></li>
                </ol>
            </div>

            <div class="row">
                <!-- Video Feed Column -->
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-video"></i> Live Video Feed (Demo)
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="video-placeholder">
                                <div class="text-center">
                                    <i class="fas fa-video fa-3x mb-3"></i>
                                    <p>Camera feed would appear here in full version</p>
                                    <small class="text-muted">Real-time ASL detection and translation</small>
                                </div>
                            </div>

                            <div class="d-flex gap-2 justify-content-center mt-3">
                                <button class="btn btn-success btn-lg" disabled>
                                    <i class="fas fa-play"></i> Start Translation (Demo)
                                </button>
                                <button class="btn btn-danger btn-lg" disabled>
                                    <i class="fas fa-stop"></i> Stop Translation
                                </button>
                                <button class="btn btn-secondary btn-lg" disabled>
                                    <i class="fas fa-trash"></i> Clear Text
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Translation Output Column -->
                <div class="col-lg-4">
                    <!-- Current Translation -->
                    <div class="card mb-3">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-comment-dots"></i> Translation Output
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="bg-light p-3 rounded" style="min-height: 200px;">
                                <p class="text-muted text-center">
                                    <i class="fas fa-hand-paper fa-2x mb-2"></i><br>
                                    In the full version, real-time ASL translation would appear here
                                </p>
                                <div class="mt-3">
                                    <small class="text-muted">Example output:</small>
                                    <div class="bg-warning bg-opacity-25 p-2 rounded mt-1">
                                        "Hello, how are you today?"
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Statistics -->
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-chart-line"></i> Demo Statistics
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row text-center">
                                <div class="col-6">
                                    <h4 class="text-primary">95%+</h4>
                                    <small>Accuracy Rate</small>
                                </div>
                                <div class="col-6">
                                    <h4 class="text-success">&lt;200ms</h4>
                                    <small>Latency</small>
                                </div>
                            </div>
                            <div class="row text-center mt-3">
                                <div class="col-6">
                                    <h4 class="text-info">1000+</h4>
                                    <small>ASL Signs</small>
                                </div>
                                <div class="col-6">
                                    <h4 class="text-warning">30+</h4>
                                    <small>FPS Processing</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features Section -->
            <div class="row mt-5">
                <div class="col-12">
                    <h3>Full System Features</h3>
                    <div class="row">
                        <div class="col-md-3">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-eye fa-2x text-primary mb-3"></i>
                                    <h5>Hand Detection</h5>
                                    <p class="small">21-point hand landmark tracking with MediaPipe</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-brain fa-2x text-success mb-3"></i>
                                    <h5>AI Recognition</h5>
                                    <p class="small">TensorFlow neural networks for sign classification</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-language fa-2x text-info mb-3"></i>
                                    <h5>Grammar Processing</h5>
                                    <p class="small">ASL-to-English sentence structure conversion</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <i class="fas fa-bolt fa-2x text-warning mb-3"></i>
                                    <h5>Real-Time</h5>
                                    <p class="small">WebSocket streaming for instant translation</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@app.route('/upload')
def upload_translation():
    """File upload translation page (demo mode)."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload Translation - ASL-to-Text AI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            .upload-area {
                border: 2px dashed #dee2e6;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                background: #f8f9fa;
                transition: all 0.3s ease;
            }
            .upload-area:hover {
                border-color: #007bff;
                background: #e3f2fd;
            }
            .demo-alert {
                border-left: 4px solid #17a2b8;
                background: #d1ecf1;
                padding: 20px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="fas fa-hands"></i> ASL-to-Text AI
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">Home</a>
                    <a class="nav-link" href="/live">Live Translation</a>
                    <a class="nav-link active" href="/upload">Upload Video</a>
                </div>
            </div>
        </nav>

        <div class="container py-4">
            <div class="demo-alert">
                <h4><i class="fas fa-info-circle"></i> Demo Mode</h4>
                <p><strong>This is a demonstration version.</strong> Video upload and AI processing require the full system with ML dependencies.</p>
                <p>To process actual ASL videos:</p>
                <ol>
                    <li>Clone: <code>git clone https://github.com/Flashinl/asl_ai.git</code></li>
                    <li>Install: <code>pip install -r requirements.txt</code></li>
                    <li>Run: <code>python web_app/app.py</code></li>
                </ol>
            </div>

            <div class="row">
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-upload"></i> Video Upload (Demo)
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="upload-area">
                                <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                                <h4>Drag & Drop Video File</h4>
                                <p class="text-muted">Supported formats: MP4, MOV, AVI, WebM</p>
                                <button class="btn btn-primary" disabled>
                                    <i class="fas fa-folder-open"></i> Choose File (Demo)
                                </button>
                            </div>

                            <div class="mt-4">
                                <h6>Demo Translation Result:</h6>
                                <div class="bg-light p-3 rounded">
                                    <div class="d-flex align-items-center mb-2">
                                        <i class="fas fa-video text-primary me-2"></i>
                                        <strong>sample_asl_video.mp4</strong>
                                        <span class="badge bg-success ms-2">Processed</span>
                                    </div>
                                    <div class="bg-white p-3 rounded border">
                                        <p class="mb-1"><strong>Translation:</strong></p>
                                        <p class="text-primary">"Hello, my name is Sarah. How are you today? I am learning sign language."</p>
                                        <small class="text-muted">
                                            <i class="fas fa-clock"></i> Processing time: 2.3s |
                                            <i class="fas fa-chart-line"></i> Confidence: 94% |
                                            <i class="fas fa-eye"></i> 15 signs detected
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-cogs"></i> Processing Features
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <h6><i class="fas fa-eye text-primary"></i> Computer Vision</h6>
                                <small class="text-muted">Hand, pose, and facial landmark detection</small>
                            </div>
                            <div class="mb-3">
                                <h6><i class="fas fa-brain text-success"></i> AI Recognition</h6>
                                <small class="text-muted">Neural network sign classification</small>
                            </div>
                            <div class="mb-3">
                                <h6><i class="fas fa-language text-info"></i> Grammar Processing</h6>
                                <small class="text-muted">ASL-to-English conversion</small>
                            </div>
                            <div class="mb-3">
                                <h6><i class="fas fa-chart-bar text-warning"></i> Quality Assessment</h6>
                                <small class="text-muted">Frame quality and confidence scoring</small>
                            </div>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-info-circle"></i> Supported Formats
                            </h5>
                        </div>
                        <div class="card-body">
                            <ul class="list-unstyled">
                                <li><i class="fas fa-check text-success"></i> MP4 (recommended)</li>
                                <li><i class="fas fa-check text-success"></i> MOV</li>
                                <li><i class="fas fa-check text-success"></i> AVI</li>
                                <li><i class="fas fa-check text-success"></i> WebM</li>
                            </ul>
                            <small class="text-muted">
                                <strong>Requirements:</strong><br>
                                • Minimum 720p resolution<br>
                                • Clear view of hands and upper body<br>
                                • Good lighting conditions<br>
                                • Maximum 5 minutes duration
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
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

@app.route('/debug')
def debug_info():
    """Debug information."""
    import os
    return jsonify({
        "working_directory": os.getcwd(),
        "template_folder": app.template_folder,
        "static_folder": app.static_folder,
        "files_in_directory": os.listdir('.'),
        "template_exists": os.path.exists(app.template_folder) if app.template_folder else False,
        "static_exists": os.path.exists(app.static_folder) if app.static_folder else False
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
