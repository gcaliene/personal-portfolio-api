from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SummarizationMessageCreate(BaseModel):
    webpage_url: str
    prompt: str
    response: Dict[str, Any]
    model: str
    tokens_used: int

class SummarizationMessageResponse(SummarizationMessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 