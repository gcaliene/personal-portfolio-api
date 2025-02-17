from pydantic import BaseModel, field_validator
from typing import Optional, Dict, List
from datetime import datetime

class ArticleBase(BaseModel):
    url: str
    source_url: str
    version: int
    sort_order: int
    type: str
    content: Dict[str, str]
    category: str
    subcategory: str
    tags: List[str]
    status: str

class ArticleCreate(ArticleBase):
    created_by: str
    updated_by: str
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('created_at', 'updated_at')
    @classmethod
    def set_datetime(cls, v):
        if v is None:
            return datetime.utcnow()
        return v

class ArticleUpdate(BaseModel):
    url: Optional[str] = None
    source_url: Optional[str] = None
    version: Optional[int] = None
    sort_order: Optional[int] = None
    type: Optional[str] = None
    content: Optional[Dict[str, str]] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None
    updated_at: Optional[datetime] = None

class ArticleInDB(ArticleBase):
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    deleted_at: Optional[datetime]
    deleted_by: Optional[str]

    @field_validator('created_at', 'updated_at', 'deleted_at')
    @classmethod
    def validate_datetime(cls, v):
        if v is None or v == 'string' or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                return None
        return v

    class Config:
        from_attributes = True 