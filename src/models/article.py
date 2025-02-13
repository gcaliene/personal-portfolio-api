from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from src.database import Base

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