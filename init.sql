CREATE TABLE IF NOT EXISTS pages (
    id BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    index_structure JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pages_url ON pages(url);
CREATE INDEX IF NOT EXISTS idx_pages_index_structure ON pages USING GIN(index_structure);