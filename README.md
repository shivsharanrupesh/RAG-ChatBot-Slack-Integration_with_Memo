# PDF RAG System with Slack Integration

A robust system for ingesting PDFs, answering questions via Retrieval-Augmented Generation (RAG), and interacting through a Slack bot with feedback capabilities.

## Features

- **Incremental PDF ingestion** with file hash deduplication
- **Session-based chat memory** for personalized interactions
- **Slack bot integration** with feedback capture
- **Comprehensive logging** and error handling
- **FastAPI backend** for question answering

## System Components

### 1. `app/ingest.py` - Incremental PDF Ingestion with File Hash Deduplication

**Key Functions:**
- `get_file_hash(filepath)`: Computes SHA-256 hash of PDF files
- `already_embedded(collection, filename, file_hash)`: Checks for existing embeddings
- `ingest_pdfs()`: Main ingestion workflow

**How Deduplication Works:**
- Files are skipped if their hash matches existing records
- Updated files replace old data with new chunks/embeddings

### 2. `app/rag_chain.py` - RAG Chain Logic & File-based Session Memory

**Session Memory:**
- `get_session_history(session_id, max_turns=10)`: Loads chat history
- `update_session_history(session_id, question, answer)`: Updates chat history

**RAG Chain Core:**
- `answer_question(question: str, session_id: str) -> dict`: Main Q&A function

### 3. `app/api.py` - FastAPI Backend

**API Endpoints:**
- `/health`: Health check
- `/ask`: Main question answering endpoint (POST)

### 4. `slack_bot.py` - Slack Bot Event Handler & Feedback Capture

**Features:**
- Listens for mentions and direct messages
- Captures emoji feedback (👍/👎)
- Logs performance metrics

### 5. Logging and Monitoring

- Comprehensive logging across all components
- Error handling and debugging support
- LLM evaluation metrics tracking

## Directory Structure

# Project Structure

├── data/               # PDF files for ingestion  
├── memory_store/       # User session histories (.json)  
├── app/                # Core backend logic  
│   ├── ingest.py       # PDF ingestion  
│   ├── rag_chain.py    # RAG logic  
│   └── api.py          # FastAPI backend  
├── slack_bot.py        # Slack integration  
├── requirements.txt    # Python dependencies  
└── *.log               # Log files  
