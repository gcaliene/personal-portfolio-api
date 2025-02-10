from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
import logging
from src.models import Article
from src.schemas.article import ArticleCreate, ArticleUpdate

logger = logging.getLogger(__name__)

class ArticleService:
    def __init__(self, db: Session):
        self.db = db

    def create_article(self, article: ArticleCreate) -> Article:
        try:
            db_article = Article(**article.dict())
            self.db.add(db_article)
            self.db.commit()
            self.db.refresh(db_article)
            return db_article
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"Article with URL '{article.url}' already exists"
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating article: {str(e)}")
            raise

    def get_article(self, url: str) -> Article:
        article = self.db.query(Article).filter(Article.url == url).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

    def update_article(self, url: str, article: ArticleUpdate) -> Article:
        db_article = self.get_article(url)
        try:
            update_data = article.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_article, key, value)
            self.db.commit()
            self.db.refresh(db_article)
            return db_article
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating article: {str(e)}")
            raise

    def delete_article(self, url: str) -> dict:
        db_article = self.get_article(url)
        try:
            self.db.delete(db_article)
            self.db.commit()
            return {"message": "Article deleted successfully"}
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting article: {str(e)}")
            raise

    def get_latest_articles(self, limit: int = 10) -> list[Article]:
        try:
            return self.db.query(Article)\
                .order_by(Article.created_at.desc())\
                .limit(limit)\
                .all()
        except Exception as e:
            logger.error(f"Error retrieving latest articles: {str(e)}")
            raise 