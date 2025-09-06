# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) application built with LangChain that ingests PDF documents into a PostgreSQL vector database using pgvector extension and provides question-answering capabilities. The system uses Google Generative AI for embeddings and chat completions.

## Architecture

The application consists of three main components:

- **src/ingest.py**: PDF document ingestion pipeline that loads, chunks, enriches, and stores documents in vector database
- **src/search.py**: Context retrieval system that performs similarity search and formats prompts for the LLM
- **src/chat.py**: Main chat interface that combines retrieval with Google Generative AI for question answering

The system uses a strict RAG approach - responses are limited to information found in the ingested documents, with explicit fallback responses when information is not available.

## Database Setup

The application requires PostgreSQL with the pgvector extension. Use Docker Compose to set up the database:

```bash
docker-compose up -d postgres
docker-compose run bootstrap_vector_ext
```

This creates a PostgreSQL container with pgvector extension enabled.

## Environment Configuration

Copy `.env.example` to `.env` and configure:

- `GOOGLE_API_KEY`: Google Generative AI API key
- `GOOGLE_EMBEDDING_MODEL`: Usually 'models/embedding-001'
- `OPENAI_API_KEY`: OpenAI API key (if using OpenAI instead)
- `OPENAI_EMBEDDING_MODEL`: Usually 'text-embedding-3-small'
- `DATABASE_URL`: PostgreSQL connection string
- `PG_VECTOR_COLLECTION_NAME`: Name for the vector collection
- `PDF_PATH`: Path to the PDF file to ingest

## Common Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Start database:
```bash
docker-compose up -d postgres
docker-compose run bootstrap_vector_ext
```

Ingest a PDF document:
```bash
python src/ingest.py
```

Start chat interface:
```bash
python src/chat.py
```

## Development Notes

- The ingestion process uses RecursiveCharacterTextSplitter with 1000 character chunks and 150 character overlap
- Vector similarity search retrieves top 10 results (k=10) for context
- The system uses Google's Gemini 2.5 Flash Lite model with temperature=0 for consistent responses
- Document metadata is cleaned during enrichment to remove empty values
- The prompt template enforces strict adherence to provided context only