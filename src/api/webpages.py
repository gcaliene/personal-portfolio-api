from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.webpage import WebpageSourceRequest, WebpageSourceResponse, WebpageSourceCreate
from src.services.webpage_service import WebpageService
from src.database import get_db
from typing import Optional

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
            source=response.text
        )
        
        db_webpage = webpage_service.create_webpage_source(webpage_create)
        
        return WebpageSourceResponse(
            url=db_webpage.url,
            title=db_webpage.title,
            source=db_webpage.source,
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