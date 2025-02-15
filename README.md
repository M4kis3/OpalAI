# OpalAI
n8n ai agent framework

Install ollama and pull mxbai embed large

install n8n or n8n ngrok on docker desktop and install ubuntu on wsl

go to google cloud console and enable, docs, drive, sheets, calendar api and oauth

go to supabase and create new project

run this sql
```
DROP FUNCTION IF EXISTS match_entries(VECTOR(1024), INT, JSONB);
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS notes;
DROP FUNCTION IF EXISTS match_news(VECTOR(1536), INT, JSONB);
DROP FUNCTION IF EXISTS match_notes(VECTOR(1536), INT, JSONB);
DROP FUNCTION IF EXISTS match_documents;
create extension if not exists vector;

-- Create table for news documents:
create table news (
  id bigserial primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(1024) -- 1536 works for OpenAI embeddings, change if needed
);

-- Create a function to search for news documents
create function match_news (
  query_embedding vector(1024),
  match_count int default null,
  filter jsonb DEFAULT '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (news.embedding <=> query_embedding) as similarity
  from news
  where metadata @> filter
  order by news.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Create table for notes documents:
create table notes (
  id bigserial primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(1024) -- 1536 works for OpenAI embeddings, change if needed
);

-- Create a function to search for notes documents
create function match_notes (
  query_embedding vector(1024),
  match_count int default null,
  filter jsonb DEFAULT '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (notes.embedding <=> query_embedding) as similarity
  from notes
  where metadata @> filter
  order by notes.embedding <=> query_embedding
  limit match_count;
end;
$$;


```
install vs code and run streamlit app with webhook
install tailscale on desktop and phone and configure
configure n8n with google credentials
