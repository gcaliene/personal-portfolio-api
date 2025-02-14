from anthropic import Anthropic
import os
from typing import Optional
import json
from sqlalchemy.orm import Session
from src.schemas.summarization import SummarizationMessageCreate
from src.services.summarization_service import SummarizationService

class AnthropicService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        with open('src/prompts/source-to-summary.md', 'r') as file:
            self.summary_prompt = file.read()

    def summarize_text(self, source_text: str, webpage_url: str, db: Session) -> Optional[dict]:
        print(source_text)
        print(self.summary_prompt)
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                messages=[{
                    "role": "user",
                    "content": f"{self.summary_prompt}\n\nWith those instructions, please return a JSON object according to the schema provided and be thorough in your analysis:\n\n{source_text}"
                }]
            )
            print("message created, storing...")
            
            # Store the message
            summarization_service = SummarizationService(db)
            message_create = SummarizationMessageCreate(
                webpage_url=webpage_url,
                prompt=self.summary_prompt,
                response=message.model_dump(),
                model=message.model,
                tokens_used=message.usage.output_tokens + message.usage.input_tokens
            )
            summarization_service.create_message(message_create)
            
            # Return the content for article creation
            # return json.loads(message.content[0].text)
            return "Stored message"
        except Exception as e:
            print(f"Error summarizing text with Anthropic: {e}")
            return None 