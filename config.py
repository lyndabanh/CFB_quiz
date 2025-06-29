import os
from dotenv import load_dotenv

load_dotenv()  # This reads .env file and makes variables available

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database Configuration
    DATABASE_PATH = 'cfb_quiz.db'
    
    # CFB API Configuration
    CFB_API_BASE_URL = 'https://api.collegefootballdata.com'
    CFB_API_KEY = os.environ.get('CFB_API_KEY')
    
    # # API Rate Limiting (CFB API has limits)
    # API_REQUESTS_PER_MINUTE = 200  # Adjust based on your API plan
    # API_TIMEOUT = 30  # seconds
    
    # # Application Settings
    # TEAMS_UPDATE_INTERVAL = 24 * 60 * 60  # 24 hours in seconds
    # DEFAULT_SEASON = 2024  # Current season
    
    # # Optional: Logging
    # LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # @staticmethod
    # def validate_config():
    #     """Validate that required config values are present"""
    #     if not Config.CFB_API_KEY:
    #         raise ValueError("CFB_API_KEY environment variable is required")
        
    #     return True
    