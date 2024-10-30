# backend/__init__.py - Application factory
from flask import Flask
from .config import Config

def create_app():
    """Initialize the core application"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize routes 
    from .routes import main 
    app.register_blueprint(main.bp)

    return app