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


# Project Documentation

## 5. Logging, Error Handling, and LLM Evaluation Metrics

- **Logging Implementation**:
  - Every script uses Python's `logging` module
  - Records events, warnings, errors, and performance metrics
  - Key metrics logged:
    - Response time
    - Number of retrieved chunks
    - LLM interaction details

- **Error Handling**:
  - Comprehensive error catching throughout all components
  - All errors are properly logged for debugging

- **LLM Evaluation Metrics**:
  - Tracked metrics include:
    - Latency
    - Retrieval count
    - Sources cited
  - Metrics are written to log files for later analysis

## 6. Requirements and README

### `requirements.txt`
- Contains all Python dependencies for:
  - PDF ingestion
  - API backend
  - Slack bot integration

### `README.md`
- **Contents**:
  - Project architecture overview
  - Detailed setup instructions
  - Step-by-step usage guide
  - Folder structure explanation
  - Startup procedures
- **Optional Expansions**:
  - Additional usage examples
  - Common patterns
  - System diagrams

## 7. Directory Structure: Why It Matters

| Directory/File       | Purpose                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `data/`              | Stores PDF files for ingestion                                         |
| `memory_store/`      | Contains per-user session chat histories (as `.json` files)            |
| `app/`               | Houses all core backend logic and ingestion scripts                    |
| `*.log` files        | Created in working directory for easy access and monitoring            |

## Summary Table

| Feature                              | Implementation Details                                  |
|--------------------------------------|--------------------------------------------------------|
| Incremental PDF ingestion & dedup    | `ingest.py` + file hash + vectorstore                  |
| Session/chat memory per user         | `rag_chain.py` + file-per-session memory               |
| Robust logging, error handling       | All files, via Python logging                          |
| Slack bot with feedback capture      | `slack_bot.py` + event listeners                       |
| API backend                          | `api.py` (FastAPI)                                     |
| Requirements, README, structure      | `requirements.txt`, `README.md`                        |


## Key Evaluation Parameters for LLM Response in RAG

### 1. Relevance
**Definition**:  
- Does the answer address the user's question?  
- Does it use the most relevant retrieved chunks?  

**Evaluation Methods**:  
- **Human Review**: Rate as "relevant", "partially relevant", or "irrelevant"  
- **Automatic**: Check if retrieved sources contain query keywords  

### 2. Groundedness (Faithfulness)  
**Definition**:  
- Is the answer based only on provided context?  
- Does it avoid hallucinations?  

**Evaluation Methods**:  
- **Human**: Flag answers with unsourced content  
- **Automatic**: N-gram overlap between answer and retrieved chunks  

### 3. Accuracy  
**Definition**:  
- Is the answer factually correct (especially for technical content)?  

**Evaluation Methods**:  
- **Expert Review**: SMEs verify answers  
- **FAQ Matching**: Compare to gold reference answers  

### 4. Completeness  
**Definition**:  
- Does the answer fully resolve the question?  
- Are key details/steps missing?  

**Evaluation Methods**:  
- **Human**: Categorize as "Fully answered", "Partial", or "Incomplete"  

### 5. Conciseness & Readability  
**Definition**:  
- Is the answer clear and free of jargon?  
- Does it avoid unnecessary details?  

### 6. Citation Quality  
**Definition**:  
- Are sources properly cited?  
- Do citations point to correct documents/sections?  

### 7. User Feedback  
**Sources**:  
- Slack reactions (👍/👎)  
- Surveys  
- Follow-up questions  

### 8. Latency  
**Metric**:  
- Response time (critical for user satisfaction)  

### 9. Escalation Rate  
**Metric**:  
- Frequency of bot-to-human handoffs  

## How To Implement Evaluation
# How To Achieve These Evaluations in Your Pipeline

## Collect Logs
Log all questions, retrieved docs, answers, sources, response time, and user ID.

Log user feedback (reactions in Slack).

## Human Review (Spot-checking)
Review random samples of Q&A pairs for quality.

Mark issues (hallucination, irrelevance, missing info, etc.).

## Automated Metrics
Track latency, answer length, retrieval count, presence of sources.

If you have reference answers (for FAQ), calculate similarity (e.g., BLEU, ROUGE, BERTScore).

## User Feedback
Analyze rate of 👍 vs. 👎, and follow-up queries after each answer.

## Business KPIs
% of queries answered without escalation.

Ticket reduction and time saved (already discussed above).

## Example Evaluation Dashboard Metrics

| Metric               | Target/Observation               |
|----------------------|----------------------------------|
| Avg. relevance       | 4.5/5 (human spot checks)       |
| Groundedness         | 98% answers cite source         |
| Accuracy             | 95%+ correct (expert review)    |
| Latency              | <3 sec avg.                     |
| User 👍 Rate         | 90%+                           |
| Escalation Rate      | <20%                           |
| Citation Correct     | 95%+ (right doc/page cited)     |
