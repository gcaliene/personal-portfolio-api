from sqlalchemy import Column, String, Text, DateTime
from src.database import Base
from datetime import datetime

class WebpageSource(Base):
    __tablename__ = "webpage_sources"

    url = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=True)
    source = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 