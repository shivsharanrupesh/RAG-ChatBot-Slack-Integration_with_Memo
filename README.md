# RAG IT Support Chatbot

This project provides a Slack-integrated Retrieval-Augmented Generation (RAG) chatbot for IT support, using company PDF knowledge base, persistent session memory, and real-time feedback.

## Structure

- `app/ingest.py`: Incremental PDF ingestion and embedding
- `app/rag_chain.py`: RAG logic and session memory
- `app/api.py`: FastAPI backend
- `slack_bot.py`: Slack bot event handler
- `data/`: Place your company IT PDFs here
- `memory_store/`: Chat/session memory per user

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Place PDFs in `data/`
3. Run `python app/ingest.py`
4. Start API: `uvicorn app.api:app --reload`
5. Configure Slack tokens and run `slack_bot.py`

Edit code for your embedding/LLM provider and company requirements.
