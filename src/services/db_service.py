from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.models import Article, Base

class DatabaseService:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def get_articles(self):
        with self.SessionLocal() as session:
            return session.query(Article).all()
    
    def get_article_by_url(self, url: str):
        with self.SessionLocal() as session:
            return session.query(Article).filter(Article.url == url).first()
    
    def article_exists(self, url: str) -> bool:
        with self.SessionLocal() as session:
            return session.query(Article).filter(Article.url == url).first() is not None

    def create_article(self, article_data: dict):
        with self.SessionLocal() as session:
            try:
                article = Article(**article_data)
                session.add(article)
                session.commit()
                session.refresh(article)
                return article
            except IntegrityError:
                session.rollback()
                raise ValueError(f"Article with URL '{article_data['url']}' already exists")
            except Exception as e:
                session.rollback()
                raise e 