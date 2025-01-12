import logging
from fastapi import FastAPI, Depends, HTTPException
from mangum import Mangum
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from models import SessionLocal, Article, Base, engine
from pydantic import BaseModel, Json
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Log the database URL
logger.info(f"Connecting to database at: {engine.url}")

# Create the schema if it does not exist
# with engine.connect() as connection:
#     connection.execute(text("CREATE SCHEMA IF NOT EXISTS portfolio"))
#
# # Create the database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

class ArticleCreate(BaseModel):
    url: str
    version: int
    sort_order: int
    type: str
    content: Json
    category: str
    subcategory: str
    tags: Json
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

@app.post("/articles/", response_model=ArticleCreate)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.get("/articles/{article_id}", response_model=ArticleCreate)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.put("/articles/{article_id}", response_model=ArticleCreate)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return {"detail": "Article deleted"}

handler = Mangum(app)