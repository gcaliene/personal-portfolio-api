import os
from dotenv import load_dotenv

load_dotenv()

def get_db_url():
    """Get the full SQLAlchemy database URL"""
    # Get PostgreSQL connection details from environment variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME", "articles")
    db_port = os.getenv("DB_PORT", "5432")
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", get_db_url())

# API configuration
API_VERSION = "v1" 