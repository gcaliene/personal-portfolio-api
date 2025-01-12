from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:password@db/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {'schema': 'portfolio'}

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), unique=True, index=True)
    version = Column(Integer)
    sort_order = Column(Integer)
    type = Column(String(50))
    content = Column(JSON)
    category = Column(String(50))
    subcategory = Column(String(50))
    tags = Column(JSON)
    status = Column(String(50))
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    created_by = Column(String(50))
    updated_by = Column(String(50))
    deleted_at = Column(TIMESTAMP)
    deleted_by = Column(String(50))