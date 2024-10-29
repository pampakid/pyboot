# backend/config.py - Configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///pyboot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-default-key')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Dictionary to map configuration names to objects
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}