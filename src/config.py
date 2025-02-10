import os
from dotenv import load_dotenv

load_dotenv()

def get_db_path():
    """Get the database path based on environment"""
    is_lambda = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
    return '/tmp/articles.db' if is_lambda else './articles.db'

def get_db_url():
    """Get the full SQLAlchemy database URL"""
    return f"sqlite:///{get_db_path()}"

# Database configuration
DATABASE_URL = get_db_url()

# API configuration
API_VERSION = "v1" 