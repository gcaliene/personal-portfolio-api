from pydantic import BaseModel
from typing import Optional, Dict, List

class ArticleBase(BaseModel):
    url: str
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
    deleted_at: Optional[str] = None
    deleted_by: Optional[str] = None

class ArticleUpdate(BaseModel):
    url: Optional[str] = None
    version: Optional[int] = None
    sort_order: Optional[int] = None
    type: Optional[str] = None
    content: Optional[Dict[str, str]] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_at: Optional[str] = None
    deleted_by: Optional[str] = None

class ArticleInDB(ArticleBase):
    created_by: str
    updated_by: str
    deleted_at: Optional[str]
    deleted_by: Optional[str]

    class Config:
        from_attributes = True 