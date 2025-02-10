import os
from flask import Flask, send_from_directory
from .routes import main
from flask_cors import CORS  # if needed

def create_app():
    # Specify the static folder and URL path (adjust relative path as needed)
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
    
    # Enable CORS if your API might be accessed from other origins (optional)
    CORS(app)
    
    # Load configuration
    app.config.from_pyfile('../config.py')
    
    # Register API blueprint (for your endpoints)
    app.register_blueprint(main, url_prefix='/api')
    
    # Serve React's index.html at the root and for any unknown route
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    return app
