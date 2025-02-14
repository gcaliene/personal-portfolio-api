from sqlalchemy import Column, String, JSON, DateTime, Integer, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.webpage import WebpageSource

class SummarizationMessage(Base):
    __tablename__ = "summarization_messages"

    id = Column(Integer, primary_key=True, index=True)
    webpage_url = Column(String, ForeignKey(WebpageSource.url, ondelete="CASCADE"), nullable=False)
    prompt = Column(Text)
    response = Column(JSON)
    model = Column(String)
    tokens_used = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add relationship to WebpageSource
    webpage = relationship("WebpageSource", backref="summarizations") 