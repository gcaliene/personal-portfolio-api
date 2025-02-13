from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class WebpageSourceBase(BaseModel):
    url: str
    title: Optional[str] = None
    source: str

class WebpageSourceCreate(WebpageSourceBase):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WebpageSourceResponse(WebpageSourceBase):
    created_at: datetime
    status_code: int
    headers: Dict[str, str]

    class Config:
        from_attributes = True

class WebpageSourceRequest(BaseModel):
    url: str 