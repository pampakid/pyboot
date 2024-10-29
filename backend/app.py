# backend/app.py - Application entry point
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .config import config

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (we'll add these later)
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # Create database tables 
    with app.app_context():
        db.create_all()

    return app

# Create the app instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run()