# backend/app.py - Application entry point
from flask import Flask
import os
from dotenv import load_dotenv
from backend.config import config
from backend.extensions import db

# Load environment variables
load_dotenv()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from backend.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    from backend.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# Create the app instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(debug=True)