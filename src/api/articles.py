from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleInDB, ArticleUrlTitle
from src.services.article_service import ArticleService
from src.database import get_db
from typing import List
from fastapi import status
from datetime import datetime

router = APIRouter(prefix="/articles", tags=["articles"])

# Example article for documentation
example_article = {
    "url": "/blog/getting-started-with-fastapi",
    "version": 1,
    "sort_order": 1,
    "type": "blog",
    "content": {
        "title": "Getting Started with FastAPI",
        "description": "A comprehensive guide to building APIs with FastAPI",
        "body": "FastAPI is a modern web framework for building APIs..."
    },
    "category": "Programming",
    "subcategory": "Python",
    "tags": ["python", "fastapi", "web development", "api"],
    "status": "published",
    "created_by": "john.doe@example.com",
    "updated_by": "john.doe@example.com",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
    "deleted_at": None,
    "deleted_by": None
}

@router.get("/latest", response_model=List[ArticleInDB])
def get_latest_articles(db: Session = Depends(get_db)):
    """
    Get the latest articles.
    """
    article_service = ArticleService(db)
    return article_service.get_latest_articles()

@router.post("/", 
    response_model=ArticleInDB,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Article created successfully",
            "content": {
                "application/json": {
                    "example": example_article
                }
            }
        }
    }
)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    """
    Create a new article with the following fields:
    - url: Unique URL for the article
    - version: Version number of the article
    - sort_order: Order for sorting articles
    - type: Type of article
    - content: Dictionary containing article content
    - category: Main category
    - subcategory: Sub-category
    - tags: List of tags
    - status: Article status
    - created_by: Author of the article
    - updated_by: Last person to update the article
    """
    print("Received article data:", article.model_dump())  # Add this line for debugging
    article_service = ArticleService(db)
    return article_service.create_article(article)

@router.get("/url-titles", response_model=List[ArticleUrlTitle])
def get_article_urls_and_titles(db: Session = Depends(get_db)):
    """
    Get URLs and titles of up to 100 most recent articles.
    Returns a list of articles with just their URLs and titles.
    """
    article_service = ArticleService(db)
    return article_service.get_urls_and_titles(limit=100) 

@router.get("/{url}", response_model=ArticleInDB)
def get_article(url: str, db: Session = Depends(get_db)):
    """
    Get a specific article by its URL.
    """
    article_service = ArticleService(db)
    return article_service.get_article(url)

@router.put("/{url}", response_model=ArticleInDB)
def update_article(url: str, article: ArticleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing article by its URL.
    All fields are optional in the update.
    """
    article_service = ArticleService(db)
    return article_service.update_article(url, article)

@router.delete("/{url}")
def delete_article(url: str, db: Session = Depends(get_db)):
    """
    Delete an article by its URL.
    """
    article_service = ArticleService(db)
    return article_service.delete_article(url)

