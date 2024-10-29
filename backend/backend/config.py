# backend/config.py - Configuration settings
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'd22f34e1e5343d04a824d4872dc75b3e')
    DEBUG = os.getenv('FLASK_DEBUG', True)