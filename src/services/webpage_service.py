from sqlalchemy.orm import Session
from src.models.webpage import WebpageSource
from src.schemas.webpage import WebpageSourceCreate
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class WebpageService:
    def __init__(self, db: Session):
        self.db = db

    def create_webpage_source(self, webpage: WebpageSourceCreate) -> WebpageSource:
        db_webpage = WebpageSource(
            url=webpage.url,
            title=webpage.title,
            source=webpage.source,
            created_at=webpage.created_at or datetime.utcnow()
        )
        self.db.add(db_webpage)
        self.db.commit()
        self.db.refresh(db_webpage)
        return db_webpage

    def get_webpage_source(self, url: str) -> WebpageSource:
        return self.db.query(WebpageSource).filter(WebpageSource.url == url).first()

    @staticmethod
    def extract_title(html_content: str) -> str:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.title.string if soup.title else None
        except:
            return None

    @staticmethod
    def fetch_webpage(url: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        return requests.get(url, headers=headers, timeout=10) 