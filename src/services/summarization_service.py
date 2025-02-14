from sqlalchemy.orm import Session
from src.models.summarization import SummarizationMessage
from src.schemas.summarization import SummarizationMessageCreate
from typing import Optional

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

    def get_messages_for_webpage(self, webpage_url: str) -> list[SummarizationMessage]:
        return self.db.query(SummarizationMessage)\
            .filter(SummarizationMessage.webpage_url == webpage_url)\
            .order_by(SummarizationMessage.created_at.desc())\
            .all()

    def get_message_by_id(self, message_id: int) -> Optional[SummarizationMessage]:
        return self.db.query(SummarizationMessage)\
            .filter(SummarizationMessage.id == message_id)\
            .first() 