from sqlalchemy import create_engine
from src.models import Base
from src.config import get_database_url

def init_db():
    engine = create_engine(get_database_url(), connect_args={"check_same_thread": False})
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!") 