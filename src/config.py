import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables at the very beginning
print("Loading environment variables from .env file...")
env_path = Path(__file__).parent.parent / '.env'
print(f"Looking for .env file at: {env_path}")
load_dotenv(dotenv_path=env_path)
print("Environment variables loaded")

def get_db_url():
    """Get the full SQLAlchemy database URL"""
    # Get PostgreSQL connection details from environment variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME", "articles")
    db_port = os.getenv("DB_PORT", "5432")
    
    # Add debugging to see what environment variables are being loaded
    print(f"Environment variables for DB connection:")
    print(f"DB_USER: {db_user}")
    print(f"DB_HOST: {db_host}")
    print(f"DB_NAME: {db_name}")
    print(f"DB_PORT: {db_port}")
    # Don't print the password for security reasons
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", get_db_url())

# API configuration
API_VERSION = "v1" 