# backend/app.py - Application entry point
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .extensions import db  # Changed to relative import
from .routes.tasks import tasks_bp  # Changed to relative import
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pyboot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(tasks_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)