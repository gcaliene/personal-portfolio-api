from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.webpage import WebpageSourceRequest, WebpageSourceResponse, WebpageSourceCreate
from src.services.webpage_service import WebpageService
from src.database import get_db
from typing import Optional
from src.services.anthropic_service import AnthropicService
from src.models.article import Article
from src.models.webpage import WebpageSource
from datetime import datetime
from sqlalchemy import func
from src.schemas.summarization import SummarizationMessageResponse, SummarizationMessageCreate
from src.services.summarization_service import SummarizationService

router = APIRouter(
    prefix="/webpages",
    tags=["webpages"],
    responses={404: {"description": "Not found"}}
)

# Add router metadata for documentation
router.tags_metadata = [
    {
        "name": "webpages",
        "description": """
        Operations with webpage sources. 
        
        You can:
        * Fetch and store webpage sources
        * Retrieve stored webpage sources
        * Extract webpage titles automatically
        """
    }
]

@router.post("/fetch", response_model=WebpageSourceResponse)
async def fetch_webpage_source(
    request: WebpageSourceRequest,
    db: Session = Depends(get_db)
):
    """
    Fetch and store a webpage source.

    This will:
    * Fetch the webpage from the given URL
    * Extract the title
    * Calculate the content size
    * Store the content in the database
    * Return the stored webpage with headers and status code

    If the webpage was previously fetched, returns the stored version.
    """
    webpage_service = WebpageService(db)
    
    try:
        # First check if we already have this webpage in our database
        existing_webpage = webpage_service.get_webpage_source(request.url)
        if existing_webpage:
            return WebpageSourceResponse(
                url=existing_webpage.url,
                title=existing_webpage.title,
                source=existing_webpage.source,
                size=existing_webpage.size,
                created_at=existing_webpage.created_at,
                status_code=200,
                headers={}
            )

        # If not in database, fetch it
        response = webpage_service.fetch_webpage(request.url)
        
        # Extract title from the HTML content
        title = webpage_service.extract_title(response.text)
        
        # Create webpage source in database
        webpage_create = WebpageSourceCreate(
            url=request.url,
            title=title,
            source=response.text,
            size=len(response.text.encode('utf-8'))
        )
        
        db_webpage = webpage_service.create_webpage_source(webpage_create)
        
        return WebpageSourceResponse(
            url=db_webpage.url,
            title=db_webpage.title,
            source=db_webpage.source,
            size=db_webpage.size,
            created_at=db_webpage.created_at,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch webpage: {str(e)}")

@router.post("/retrieve", response_model=WebpageSourceResponse)
async def get_stored_webpage(
    request: WebpageSourceRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieve a previously stored webpage source.

    Request Body:
    * url: The URL of the webpage to retrieve

    Returns:
    * The webpage content
    * Title
    * Creation timestamp
    * Original status code and headers

    Raises:
    * 404 if the webpage was not found in the database
    """
    webpage_service = WebpageService(db)
    webpage = webpage_service.get_webpage_source(request.url)
    
    if webpage is None:
        raise HTTPException(status_code=404, detail="Webpage not found")
        
    return WebpageSourceResponse(
        url=webpage.url,
        title=webpage.title,
        source=webpage.source,
        created_at=webpage.created_at,
        status_code=200,
        headers={}
    )

@router.post("/summarize", response_model=dict)
async def summarize_webpage(request: WebpageSourceRequest, db: Session = Depends(get_db)):
    webpage = db.query(WebpageSource).filter(WebpageSource.url == request.url).first()
    if not webpage:
        raise HTTPException(status_code=404, detail="Webpage not found")

    # First try to get existing summary
    summarization_service = SummarizationService(db)
    existing_summary = summarization_service.get_latest_summary_content(webpage.url)
    if existing_summary:
        print('existing_summary. url: ', existing_summary.get('url', webpage.url))
        # Create article directly from the JSON summary
        article = Article(
            url=existing_summary.get('url', webpage.url),
            version=existing_summary.get('version', 1),
            sort_order=existing_summary.get('sort_order', 1),
            type=existing_summary.get('type', 'summary'),
            content=existing_summary.get('content', ''),
            category=existing_summary.get('category', 'web_summaries'),
            subcategory=existing_summary.get('subcategory', 'auto_generated'),
            tags=existing_summary.get('tags', ["summary", "ai_generated"]),
            status=existing_summary.get('status', 'published'),
            created_by=existing_summary.get('created_by', 'system'),
            updated_by=existing_summary.get('updated_by', 'system')
        )
    else:
        print('no existing summary. generating new one...')
        # Generate new summary if none exists
        anthropic_service = AnthropicService()
        summary = anthropic_service.summarize_text(webpage.source, webpage.url, db)
        
        if not summary:
            raise HTTPException(status_code=500, detail="Failed to generate summary")
            
        # Try to get the newly created summary
        existing_summary = summarization_service.get_latest_summary_content(webpage.url)
        if not existing_summary:
            raise HTTPException(status_code=500, detail="Failed to retrieve generated summary")
            
        # Create article from the newly generated summary
        article = Article(
            url=existing_summary.get('url', webpage.url),
            version=existing_summary.get('version', 1),
            sort_order=existing_summary.get('sort_order', 1),
            type=existing_summary.get('type', 'summary'),
            content=existing_summary.get('content', ''),
            category=existing_summary.get('category', 'web_summaries'),
            subcategory=existing_summary.get('subcategory', 'auto_generated'),
            tags=existing_summary.get('tags', ["summary", "ai_generated"]),
            status=existing_summary.get('status', 'published'),
            created_by=existing_summary.get('created_by', 'system'),
            updated_by=existing_summary.get('updated_by', 'system')
        )
    
    db.add(article)
    db.commit()
    db.refresh(article)

    return {"message": "Summary created successfully", "article_id": article.url}

@router.post("/summarizations", response_model=list[SummarizationMessageResponse])
async def get_webpage_summarizations(
    request: WebpageSourceRequest,
    db: Session = Depends(get_db)
):
    """
    Get all summarization attempts for a webpage.
    
    Request Body:
    * url: The URL of the webpage to retrieve summarizations for
    
    Returns:
    * List of summarization messages with their prompts, responses, and token usage
    """
    summarization_service = SummarizationService(db)
    messages = summarization_service.get_messages_for_webpage(request.url)
    
    if not messages:
        raise HTTPException(status_code=404, detail="No summarizations found for this webpage")
        
    return messages

@router.post("/summarizations/store", response_model=SummarizationMessageResponse)
async def store_summarization_message(
    message: SummarizationMessageCreate,
    db: Session = Depends(get_db)
):
    """
    Store a new summarization message.
    
    Request Body:
    * webpage_url: URL of the webpage
    * prompt: The prompt used
    * response: The response from the model
    * model: Model name used
    * tokens_used: Number of tokens used
    """
    summarization_service = SummarizationService(db)
    stored_message = summarization_service.create_message(message)
    return stored_message

@router.post("/summarizations/{message_id}", response_model=SummarizationMessageResponse)
async def get_summarization_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific summarization message by ID.
    """
    summarization_service = SummarizationService(db)
    message = summarization_service.get_message_by_id(message_id)
    
    if not message:
        raise HTTPException(status_code=404, detail="Summarization message not found")
        
    return message 