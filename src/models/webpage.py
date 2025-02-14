from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.sql import func
from src.database import Base

class WebpageSource(Base):
    __tablename__ = "webpage_sources"
    
    url = Column(String, primary_key=True, index=True)
    title = Column(String)
    source = Column(Text)
    size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 