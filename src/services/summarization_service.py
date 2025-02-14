from sqlalchemy.orm import Session
from src.models.summarization import SummarizationMessage
from src.schemas.summarization import SummarizationMessageCreate
from typing import Optional
import json

class SummarizationService:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message: SummarizationMessageCreate) -> SummarizationMessage:
        db_message = SummarizationMessage(
            webpage_url=message.webpage_url,
            prompt=message.prompt,
            response=message.response,
            model=message.model,
            tokens_used=message.tokens_used
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_latest_summary_content(self, webpage_url: str) -> Optional[dict]:
        """Get the latest summary content for a webpage."""
        message = self.db.query(SummarizationMessage)\
            .filter(SummarizationMessage.webpage_url == webpage_url)\
            .order_by(SummarizationMessage.created_at.desc())\
            .first()
        
        if not message:
            return None
            
        try:
            # Get the content from the response
            response = message.response
            content_text = response.get('content', [])[0].get('text', '')
            
            # Find the JSON object in the content text
            start_idx = content_text.find('{')
            if start_idx == -1:
                return None
                
            json_str = content_text[start_idx:]
            return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing summary content: {e}")
            return None

    def get_messages_for_webpage(self, webpage_url: str) -> list[SummarizationMessage]:
        return self.db.query(SummarizationMessage)\
            .filter(SummarizationMessage.webpage_url == webpage_url)\
            .order_by(SummarizationMessage.created_at.desc())\
            .all()

    def get_message_by_id(self, message_id: int) -> Optional[SummarizationMessage]:
        return self.db.query(SummarizationMessage)\
            .filter(SummarizationMessage.id == message_id)\
            .first() 