# OpalAI
n8n ai agent framework

Install ollama and pull mxbai embed large

install n8n or n8n ngrok on docker desktop and install ubuntu on wsl

go to google cloud console and enable, docs, drive, sheets, calendar api and oauth

go to supabase and create new project

run this sql
```
DROP FUNCTION IF EXISTS match_entries(VECTOR(1024), INT, JSONB);
DROP table news;
DROP table notes;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE news (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  metadata JSONB,
  embedding VECTOR(1024) -- Adjust the dimension based on your embedding model
);
CREATE TABLE notes (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  metadata JSONB,
  embedding VECTOR(1024) -- Adjust the dimension based on your embedding model
);
CREATE FUNCTION match_entries (
  query_embedding VECTOR(1024),
  match_count INT DEFAULT 10,
  filter JSONB DEFAULT '{}'
) RETURNS TABLE (
  id BIGINT,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    id,
    content,
    metadata,
    1 - (embedding <=> query_embedding) AS similarity
  FROM (
    SELECT id, content, metadata, embedding FROM news
    UNION ALL
    SELECT id, content, metadata, embedding FROM notes
  ) AS combined
  WHERE metadata @> filter
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
CREATE INDEX ON news USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON notes USING ivfflat (embedding vector_cosine_ops);

```
install vs code and run streamlit app with webhook
install tailscale on desktop and phone and configure
configure n8n with google credentials
