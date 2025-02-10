import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.db_service import DatabaseService
from src.config import DATABASE_URL

def main():
    # Initialize database service
    db_service = DatabaseService(DATABASE_URL)
    
    # Example: List all articles
    articles = db_service.get_articles()
    for article in articles:
        print(f"Article: {article.url} - {article.category}")
    
    # Example: Create new article
    new_article = {
        "url": "test-article",
        "version": 1,
        "sort_order": 1,
        "type": "blog",
        "content": {"title": "Test", "body": "Test content"},
        "category": "test",
        "subcategory": "example",
        "tags": ["test", "example"],
        "status": "draft",
        "created_by": "script",
        "updated_by": "script"
    }
    
    db_service.create_article(new_article)

if __name__ == "__main__":
    main() 