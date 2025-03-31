import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # SpyCloud API configuration
    SPYCLOUD_API_KEY = os.getenv('SPYCLOUD_API_KEY')
    SPYCLOUD_API_ENDPOINT = os.getenv('SPYCLOUD_API_ENDPOINT')
    
    @staticmethod
    def init_app(app):
        pass 