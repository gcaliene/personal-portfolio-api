from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleInDB
from src.services.article_service import ArticleService
from src.database import get_db
from typing import List

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/latest", response_model=List[ArticleInDB])
def get_latest_articles(db: Session = Depends(get_db)):
    article_service = ArticleService(db)
    return article_service.get_latest_articles()

@router.post("/", response_model=ArticleInDB)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    article_service = ArticleService(db)
    return article_service.create_article(article)

@router.get("/{url}", response_model=ArticleInDB)
def get_article(url: str, db: Session = Depends(get_db)):
    article_service = ArticleService(db)
    return article_service.get_article(url)

@router.put("/{url}", response_model=ArticleInDB)
def update_article(url: str, article: ArticleUpdate, db: Session = Depends(get_db)):
    article_service = ArticleService(db)
    return article_service.update_article(url, article)

@router.delete("/{url}")
def delete_article(url: str, db: Session = Depends(get_db)):
    article_service = ArticleService(db)
    return article_service.delete_article(url) 