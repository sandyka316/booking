import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-bookspace'
    
    # Simplified database path - store in project root
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///bookspace.db'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Rest of the config remains the same...

    
    # Flask-WTF CSRF Protection
    WTF_CSRF_ENABLED = True
    
    # Session management
    PERMANENT_SESSION_LIFETIME = timedelta(days=14)
    
    # File uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Application settings
    SPACES_PER_PAGE = 12
    BOOKING_START_HOUR = 7  # 7 AM
    BOOKING_END_HOUR = 22   # 10 PM
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
class ProductionConfig(Config):
    DEBUG = False
    # Use environment variables for production settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}