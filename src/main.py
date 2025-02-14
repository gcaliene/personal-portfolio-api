from fastapi import FastAPI
from mangum import Mangum
from src.api import articles, webpages
from src.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Content API",
    description="API for managing content and webpages",
    version="1.0.0"
)

# Include routers
app.include_router(articles.router)
app.include_router(webpages.router)

# Handler for AWS Lambda
handler = Mangum(app) 