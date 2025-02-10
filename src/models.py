# Move your existing models.py content here if it's not already in src/ 

import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use /tmp in Lambda, local directory otherwise
is_lambda = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
db_path = '/tmp/articles.db' if is_lambda else './articles.db'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    url = Column(String, primary_key=True, index=True)
    version = Column(Integer)
    sort_order = Column(Integer)
    type = Column(String)
    content = Column(JSON)
    category = Column(String)
    subcategory = Column(String)
    tags = Column(JSON)
    status = Column(String)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(String, nullable=True)
    deleted_by = Column(String, nullable=True) 