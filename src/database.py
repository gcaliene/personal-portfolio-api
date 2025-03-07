import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from src.config import DATABASE_URL

logger = logging.getLogger(__name__)

Base = declarative_base()


STAGE = os.getenv("STAGE", "dev")

logger.info(f"Using database: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Enables automatic reconnection
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
    
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    # Verify tables were created
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Created tables: {tables}")
    
    logger.info(f"Database initialized in {STAGE} mode") 