from sqlalchemy import Column, String, Text, Integer, DateTime
from .base import Base

class WebpageSource(Base):
    __tablename__ = "webpage_sources"
    
    url = Column(String, primary_key=True, index=True)
    title = Column(String)
    source = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime) 