import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Use environment variable if available, otherwise use SQLite
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Use /tmp in Lambda, local directory otherwise
    is_lambda = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
    db_path = '/tmp/articles.db' if is_lambda else './articles.db'
    DATABASE_URL = f"sqlite:///{db_path}"

# Create engine with appropriate connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=True  # Set to True for debugging SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 