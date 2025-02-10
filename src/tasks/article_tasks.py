from src.services.db_service import DatabaseService
from src.config import DATABASE_URL
from src.models import Article
import logging

logger = logging.getLogger(__name__)

def cleanup_old_articles():
    db_service = DatabaseService(DATABASE_URL)
    try:
        with db_service.SessionLocal() as session:
            # Example: Delete articles older than 30 days
            from datetime import datetime, timedelta
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            old_articles = session.query(Article)\
                .filter(Article.created_at < thirty_days_ago)\
                .all()
            
            for article in old_articles:
                logger.info(f"Deleting old article: {article.url}")
                session.delete(article)
            
            session.commit()
    except Exception as e:
        logger.error(f"Error cleaning up old articles: {e}") 