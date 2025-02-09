CREATE SCHEMA IF NOT EXISTS portfolio;

SET search_path TO portfolio;

-- Create the articles table if it doesn't exist
CREATE TABLE IF NOT EXISTS portfolio.articles (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) UNIQUE NOT NULL,
    version INTEGER,
    sort_order INTEGER,
    type VARCHAR(50),
    content JSONB,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    tags JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted_at TIMESTAMP,
    deleted_by VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_articles_url ON portfolio.articles(url); 