import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the RPA solution"""
    
    def __init__(self):
        # Project information
        self.PROJECT_INFO = {
            'name': 'rpa_automation',
            'version': '1.0.0',
            'description': 'RPA Automation Framework'
        }

        # Application paths
        self.APP_PATHS = {
            'input_folder': 'data/input',
            'output_folder': 'data/output',
            'temp_folder': 'data/temp',
            'logs_folder': 'logs'
        }

        # Processing settings
        self.SETTINGS = {
            'retry_attempts': 3,
            'timeout_seconds': 30,
            'debug_mode': True
        }

        # Database connection settings
        self.DB_CONFIG = {
            'enabled': True,
            'host': os.getenv('DB_HOST', 'db.supabase.co'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'schema': self.PROJECT_INFO['name']
        }

    def get_db_connection_string(self):
        """Generate PostgreSQL connection string from settings"""
        if not self.DB_CONFIG['enabled']:
            return None
        return f"postgresql://{self.DB_CONFIG['user']}:{self.DB_CONFIG['password']}@{self.DB_CONFIG['host']}:{self.DB_CONFIG['port']}/{self.DB_CONFIG['database']}"