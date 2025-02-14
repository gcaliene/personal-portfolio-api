from sqlalchemy.orm import Session
from src.models.webpage import WebpageSource
from src.schemas.webpage import WebpageSourceCreate
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys

class WebpageService:
    def __init__(self, db: Session):
        self.db = db

    def create_webpage_source(self, webpage: WebpageSourceCreate) -> WebpageSource:
        # Clean the source HTML before storing
        cleaned_source = self.clean_html_content(webpage.source)
        
        db_webpage = WebpageSource(
            url=webpage.url,
            title=webpage.title,
            source=cleaned_source,
            size=len(cleaned_source.encode('utf-8')),  # Size in bytes
            created_at=webpage.created_at or datetime.utcnow()
        )
        self.db.add(db_webpage)
        self.db.commit()
        self.db.refresh(db_webpage)
        return db_webpage

    @staticmethod
    def clean_html_content(html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove all script tags
        for script in soup.find_all('script'):
            script.decompose()
            
        # Remove all style tags
        for style in soup.find_all('style'):
            style.decompose()
            
        # Get the cleaned text content
        cleaned_text = ' '.join(soup.stripped_strings)
        return cleaned_text

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