import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Template settings
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    
    # Logging settings
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_ROTATION = os.getenv('LOG_ROTATION', '500 MB')
    LOG_RETENTION = os.getenv('LOG_RETENTION', '10 days')
    
    # PDF settings
    PDF_DPI = int(os.getenv('PDF_DPI', 300))
    PDF_FORMAT = os.getenv('PDF_FORMAT', 'A4')
    
    # Image settings
    IMAGE_FORMAT = os.getenv('IMAGE_FORMAT', 'PNG')
    IMAGE_QUALITY = int(os.getenv('IMAGE_QUALITY', 95)) 