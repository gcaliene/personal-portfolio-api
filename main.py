import logging
from fastapi import FastAPI, Depends, HTTPException
from mangum import Mangum
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import SessionLocal, Article, Base, engine
from pydantic import BaseModel, Json
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

logger.info(f"Connecting to database at: {engine.url}")

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Create all tables
    Base.metadata.create_all(bind=engine)

class ArticleCreate(BaseModel):
    url: str
    version: int
    sort_order: int
    type: str
    content: Dict[str, str]  # Use Dict to parse JSON object
    category: str
    subcategory: str
    tags: List[str]  # Use List to parse JSON array
    status: str
    created_by: str
    updated_by: str
    deleted_at: Optional[str] = None
    deleted_by: Optional[str] = None

class ArticleUpdate(BaseModel):
    url: Optional[str] = None
    version: Optional[int] = None
    sort_order: Optional[int] = None
    type: Optional[str] = None
    content: Optional[Json] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[Json] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_at: Optional[str] = None
    deleted_by: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/databases")
def list_databases():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
        databases = [row[0] for row in result]
    return {"databases": databases}

@app.get("/schemas")
def list_schemas():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT schema_name FROM information_schema.schemata;"))
        schemas = [row[0] for row in result]
    return {"schemas": schemas}

@app.get("/tables")
def list_tables():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT table_schema, table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE';"))
        tables = [{"schema": row[0], "table": row[1]} for row in result]
    return {"tables": tables}

@app.post("/article/", response_model=ArticleCreate)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
@app.get("/article/{url}", response_model=ArticleCreate)
def read_article(url: str, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.url == url).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.put("/article/{url}", response_model=ArticleCreate)
def update_article(url: str, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.url == url).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.delete("/article/{url}")
def delete_article(url: str, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.url == url).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return {"detail": "Article deleted"}

@app.get("/articles/latest", response_model=List[ArticleCreate])
def get_latest_articles(db: Session = Depends(get_db)):
    latest_articles = db.query(Article).order_by(Article.created_at.desc()).limit(10).all()
    return latest_articles

handler = Mangum(app)