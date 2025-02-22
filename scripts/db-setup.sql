DO $$
BEGIN
CREATE SCHEMA IF NOT EXISTS portfolio;
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'portfolio' AND table_name = 'articles') THEN
CREATE TABLE IF NOT EXISTS portfolio.articles (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) UNIQUE,
    version INT,
    sort_order INT,
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
CREATE INDEX idx_items_url ON portfolio.articles (url);
END IF;
END $$;