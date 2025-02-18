import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

load_dotenv()

# Use environment variable if available, otherwise use SQLite
DATABASE_URL = os.getenv("DATABASE_URL")
STAGE = os.getenv("STAGE", "dev")

if not DATABASE_URL:
    # Use /tmp in Lambda, local directory otherwise
    is_lambda = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
    db_path = '/tmp/articles.db' if is_lambda else './articles.db'
    DATABASE_URL = f"sqlite:///{db_path}"

logger.info(f"Using database: {DATABASE_URL}")

# Create engine with appropriate connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Set to True for debugging SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database by creating all tables."""
    logger.info("Starting database initialization...")
    
    # Import models in correct order for foreign key relationships
    from src.models.webpage import WebpageSource  # First, as it's referenced by others
    from src.models.article import Article
    from src.models.summarization import SummarizationMessage  # Last, as it depends on WebpageSource
    
    # In development, drop and recreate all tables -- Comment if you don't want to drop and recreate the tables locally
    # if STAGE == "dev":
    #     logger.info("Development environment detected - dropping all tables")
    #     Base.metadata.drop_all(bind=engine)
    
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    # Verify tables were created
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Created tables: {tables}")
    
    logger.info(f"Database initialized in {STAGE} mode") 