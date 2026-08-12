# 🤖 AI Document Processing & RAG System

A production-style **AI Document Processing and Retrieval-Augmented Generation (RAG) system** built with **FastAPI, PostgreSQL, pgvector, LangChain, Groq, OCR, SentenceTransformers, and Docker**.

The system allows users to upload PDF documents, automatically extract text, perform OCR on scanned documents, generate embeddings, store them in PostgreSQL using pgvector, perform semantic search, ask questions using RAG, generate AI summaries, extract structured JSON data, provide source citations, and download generated reports.

This project is designed as both a **real-world AI backend application** and an **interview preparation project** for Python, FastAPI, Backend, Generative AI, LLM, RAG, Vector Database, and AI Engineering roles.

---

## 🚀 Key Features

* 📄 PDF document upload
* 🔍 Automatic PDF text extraction
* 🖼️ OCR for scanned/image-based PDFs
* ✂️ Intelligent document chunking
* 🧠 Embedding generation using SentenceTransformers
* 🗄️ PostgreSQL database
* 🔢 pgvector for vector similarity search
* 🔗 LangChain-based RAG pipeline
* 🤖 Groq LLM integration
* 🔎 Semantic document search
* 💬 Context-aware question answering
* 📚 Source/page-level citations
* 📝 AI document summarization
* 📦 Structured JSON extraction
* 📑 Downloadable PDF reports
* 🔐 JWT authentication and authorization
* ⚡ Asynchronous document processing
* 🐳 Docker and Docker Compose
* 🧪 Pytest-based testing
* 📊 RAG evaluation
* 📝 Structured logging
* 🛡️ Production-oriented error handling

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Client        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │     REST APIs       │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │ PDF / OCR   │       │ PostgreSQL  │       │   Groq LLM  │
       │ Processing  │       │ + pgvector  │       │             │
       └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
              │                     │                     │
              ▼                     ▼                     │
       ┌─────────────┐       ┌─────────────┐              │
       │  Chunking   │       │  Embeddings │              │
       └──────┬──────┘       └──────┬──────┘              │
              │                     │                     │
              └──────────────┬──────┘                     │
                             ▼                            │
                    ┌─────────────────┐                   │
                    │    LangChain    │◄──────────────────┘
                    │   RAG Pipeline  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Answer + Sources│
                    │   + Citations   │
                    └─────────────────┘
```

---

## 🔄 Document Processing Pipeline

```text
PDF Upload
     │
     ▼
File Validation
     │
     ▼
PDF Text Extraction
     │
     ▼
Is sufficient text available?
     │
   ┌─┴─────────────┐
   │               │
  YES              NO
   │               │
   │               ▼
   │              OCR
   │               │
   └───────┬───────┘
           ▼
      Text Cleaning
           │
           ▼
       Chunking
           │
           ▼
     Embeddings
           │
           ▼
 PostgreSQL + pgvector
           │
           ▼
     Document READY
```

---

# 🧠 RAG Pipeline

The question-answering pipeline works as follows:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
pgvector Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
LangChain RAG Pipeline
      │
      ▼
Context Construction
      │
      ▼
Groq LLM
      │
      ▼
Generated Answer
      │
      ▼
Source Citations
```

The system is designed to answer questions using retrieved document context rather than allowing the LLM to freely generate unsupported information.

---

# 🛠️ Technology Stack

## Backend

* Python 3.12+
* FastAPI
* Pydantic
* SQLAlchemy 2.0
* Alembic
* Uvicorn

## Database

* PostgreSQL
* pgvector

## AI / LLM

* Groq
* LangChain
* SentenceTransformers
* `all-MiniLM-L6-v2`

## Document Processing

* PyMuPDF
* Tesseract OCR
* Pillow
* OpenCV

## Infrastructure

* Docker
* Docker Compose

## Testing

* Pytest
* FastAPI TestClient

---

# 📂 Project Structure

```text
ai-document-processing/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── documents.py
│   │       ├── search.py
│   │       ├── chat.py
│   │       ├── extraction.py
│   │       └── reports.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── document_page.py
│   │   └── document_chunk.py
│   │
│   ├── schemas/
│   │   ├── document.py
│   │   ├── search.py
│   │   ├── chat.py
│   │   └── extraction.py
│   │
│   ├── repositories/
│   │   ├── document_repository.py
│   │   └── chunk_repository.py
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── ocr_service.py
│   │   ├── chunking_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_search_service.py
│   │   ├── rag_service.py
│   │   ├── llm_service.py
│   │   ├── summary_service.py
│   │   ├── extraction_service.py
│   │   └── report_service.py
│   │
│   └── workers/
│       └── document_worker.py
│
├── migrations/
│
├── tests/
│   ├── test_documents.py
│   ├── test_search.py
│   ├── test_rag.py
│   └── test_extraction.py
│
├── uploads/
├── reports/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── alembic.ini
├── README.md
└── .gitignore
```

---

# 📋 Core Features

## 1. PDF Upload

Endpoint:

```http
POST /api/v1/documents/upload
```

The API:

1. Validates the PDF.
2. Checks file size.
3. Generates a document ID.
4. Stores document metadata.
5. Saves the file.
6. Starts document processing.
7. Returns the processing status.

Example:

```json
{
    "document_id": "uuid",
    "filename": "annual_report.pdf",
    "status": "processing"
}
```

---

# 2. PDF Text Extraction

Text-based PDFs are processed using **PyMuPDF**.

The extracted content retains page information so that the RAG system can later generate page-level citations.

---

# 3. OCR

Scanned PDFs are automatically detected when insufficient text is extracted.

```text
Scanned PDF
     ↓
PDF → Images
     ↓
Tesseract OCR
     ↓
Extracted Text
     ↓
Page Metadata
```

Each page stores:

```json
{
    "page": 4,
    "extraction_method": "ocr"
}
```

---

# 4. Document Chunking

Documents are divided into smaller chunks before embedding.

Example configuration:

```text
chunk_size = 800
chunk_overlap = 150
```

Each chunk maintains metadata:

```json
{
    "document_id": "...",
    "page_number": 5,
    "chunk_index": 12
}
```

---

# 5. Embeddings

Embeddings are generated using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The resulting vectors are stored in PostgreSQL using pgvector.

```text
Document Chunk
      ↓
SentenceTransformer
      ↓
384-dimensional Embedding
      ↓
PostgreSQL + pgvector
```

---

# 6. Semantic Search

Endpoint:

```http
POST /api/v1/search
```

Example request:

```json
{
    "query": "What are the company's revenue figures?",
    "document_id": "uuid",
    "top_k": 5
}
```

The system:

```text
Query
 ↓
Embedding
 ↓
pgvector
 ↓
Similarity Search
 ↓
Top-K Chunks
```

---

# 7. RAG Question Answering

Endpoint:

```http
POST /api/v1/chat
```

Example:

```json
{
    "document_id": "uuid",
    "question": "What was the company's revenue in 2025?"
}
```

The RAG system retrieves relevant document chunks and passes them through the LangChain pipeline to the Groq LLM.

The model is instructed to:

* Answer only from retrieved context.
* Avoid unsupported information.
* Say when the information cannot be found.
* Provide source citations.
* Include page numbers where available.

---

# 8. LangChain Integration

LangChain is used as the orchestration layer for the LLM/RAG workflow.

Example conceptual flow:

```text
Retriever
    ↓
Retrieved Documents
    ↓
Prompt Template
    ↓
Groq Chat Model
    ↓
Structured / Natural Language Response
```

LangChain helps organize:

* Document retrieval
* Prompt construction
* LLM invocation
* RAG chains
* Structured output
* Prompt templates

The underlying vector database remains **PostgreSQL + pgvector**.

---

# 9. Source Citations

Every RAG response should contain source information.

Example:

```text
The company's revenue increased by 18% in 2025.

[Source: annual_report.pdf, Page 12]
```

Internally:

```json
{
    "citation_id": 1,
    "document_id": "...",
    "chunk_id": "...",
    "page_number": 12,
    "filename": "annual_report.pdf"
}
```

The system should only generate citations from chunks actually retrieved during the RAG process.

---

# 10. AI Document Summary

Endpoint:

```http
POST /api/v1/documents/{document_id}/summary
```

The generated summary contains:

* Executive Summary
* Key Points
* Important Facts
* Important Numbers
* Risks / Issues
* Conclusion

For large documents:

```text
Document
    ↓
Chunks
    ↓
Individual Summaries
    ↓
Combined Summary
    ↓
Final AI Summary
```

This avoids unnecessarily sending the entire document to the LLM.

---

# 11. Structured JSON Extraction

Endpoint:

```http
POST /api/v1/documents/{document_id}/extract
```

Example request:

```json
{
    "fields": [
        "company_name",
        "revenue",
        "employees",
        "founded_year",
        "headquarters"
    ]
}
```

Example response:

```json
{
    "company_name": "Example Corp",
    "revenue": "$14.2 million",
    "employees": 350,
    "founded_year": 2018,
    "headquarters": "New York"
}
```

The output is validated using **Pydantic**.

The system should distinguish between:

```text
FOUND
NOT_FOUND
UNCERTAIN
```

Missing information should not be fabricated by the LLM.

---

# 12. PDF Report Generation

Endpoint:

```http
GET /api/v1/documents/{document_id}/report
```

The generated report can contain:

```text
Document Information
        ↓
Executive Summary
        ↓
Extracted Information
        ↓
Important Findings
        ↓
Questions & Answers
        ↓
Source Citations
        ↓
Processing Information
```

---

# 🔐 Authentication & Security

The application includes production-oriented security practices:

* JWT authentication
* Password hashing
* User authorization
* User-specific documents
* File type validation
* File size validation
* Safe filenames
* Path traversal protection
* Environment-based secrets
* CORS configuration
* Request validation
* Global exception handling

Users should only be able to access their own documents.

---

# 🗄️ Database Design

### Users

```text
users
├── id
├── email
├── password_hash
├── created_at
└── updated_at
```

### Documents

```text
documents
├── id
├── user_id
├── filename
├── file_path
├── file_size
├── mime_type
├── status
├── processing_error
├── created_at
└── updated_at
```

### Document Pages

```text
document_pages
├── id
├── document_id
├── page_number
├── text
├── extraction_method
└── created_at
```

### Document Chunks

```text
document_chunks
├── id
├── document_id
├── page_id
├── chunk_index
├── content
├── embedding
├── metadata
└── created_at
```

The `embedding` column uses pgvector.

---

# 🐳 Docker

The application is containerized using Docker.

Main services:

```text
┌─────────────────────┐
│       FastAPI       │
│        API          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│      + pgvector     │
└─────────────────────┘
```

Groq is accessed through its API.

---

# ⚙️ Environment Variables

Create a `.env` file:

```env
APP_NAME=AI Document Processing System
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/document_ai

GROQ_API_KEY=your_groq_api_key

LLM_MODEL=your_groq_model

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

UPLOAD_DIR=uploads
REPORT_DIR=reports

MAX_FILE_SIZE_MB=20
TOP_K=5
CHUNK_SIZE=800
CHUNK_OVERLAP=150
```

**Never commit your real `GROQ_API_KEY` to GitHub.**

Add `.env` to `.gitignore`.

---

# ▶️ Running the Project

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-document-processing-rag.git

cd ai-document-processing-rag
```

## 2. Create Environment File

```bash
cp .env.example .env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_api_key
```

## 3. Start Docker

```bash
docker compose up --build
```

## 4. API Documentation

Once the application is running:

```text
http://localhost:8000/docs
```

FastAPI automatically provides interactive Swagger API documentation.

---

# 🧪 Testing

Run:

```bash
pytest
```

Tests cover:

### Unit Tests

* PDF extraction
* OCR detection
* Chunking
* Embedding generation
* Citation creation
* JSON validation

### API Tests

* Authentication
* PDF upload
* Document retrieval
* Search
* Chat
* Summary
* Extraction
* Report generation

### RAG Tests

```text
Question
   ↓
Retrieval
   ↓
Context
   ↓
LLM
   ↓
Answer
   ↓
Citation
```

Also test questions whose answers do not exist in the uploaded document.

Expected behavior:

```text
I could not find this information in the provided document.
```

---

# 📊 RAG Evaluation

The project includes a foundation for evaluating RAG performance.

## Retrieval Metrics

* Recall@K
* Precision@K
* MRR

## Generation Metrics

* Faithfulness
* Answer Relevance
* Citation Correctness

Example evaluation record:

```json
{
    "question": "What was revenue in 2025?",
    "expected_page": 12,
    "expected_answer": "$14.2 million"
}
```

---

# ⚡ Performance & Scalability

The system is designed with scalability in mind.

### Large Documents

Use background processing instead of blocking the upload request.

### Embeddings

Generate embeddings in batches.

### Vector Search

Use pgvector indexes for efficient similarity search.

### LLM Context

Only send relevant retrieved chunks to the LLM.

### Database

Use appropriate PostgreSQL indexes.

### Caching

Redis can be introduced for frequently repeated queries.

### Workers

Celery can be introduced for large-scale document processing.

---

# 📈 Future Improvements

Planned advanced features:

* [ ] Hybrid Search
* [ ] BM25 + Vector Search
* [ ] Cross-Encoder Reranking
* [ ] Query Rewriting
* [ ] Multi-Query Retrieval
* [ ] Metadata Filtering
* [ ] Conversation Memory
* [ ] Streaming LLM Responses
* [ ] Redis Caching
* [ ] Celery Workers
* [ ] API Rate Limiting
* [ ] Observability
* [ ] RAG Evaluation Dashboard
* [ ] Advanced hallucination detection
* [ ] Multi-document RAG

---

# 🎯 Interview Preparation

This project is specifically designed to prepare for **AI Backend / Generative AI / LLM Engineer / Python Backend Engineer** interviews.

## FastAPI

* Why FastAPI?
* Async vs synchronous programming?
* Dependency Injection?
* Pydantic validation?
* Middleware?
* Background tasks?
* API versioning?

## PostgreSQL

* Why PostgreSQL?
* Relational vs NoSQL databases?
* Transactions?
* Indexes?
* Relationships?
* Connection pooling?

## pgvector

* What is vector search?
* How does cosine similarity work?
* What is an embedding?
* HNSW vs IVFFlat?
* Why pgvector instead of FAISS?
* How does vector indexing improve retrieval?

## RAG

* What is RAG?
* Why do we chunk documents?
* How do you select chunk size?
* What is chunk overlap?
* How are embeddings generated?
* How does semantic search work?
* How do you reduce hallucinations?
* How do you evaluate RAG?

## LangChain

* Why use LangChain?
* What problem does LangChain solve?
* What is a Retriever?
* What is a PromptTemplate?
* What is an LLM chain?
* How does a RAG chain work?
* When would you avoid LangChain and implement the pipeline directly?

## OCR

* When do you need OCR?
* How can you detect scanned PDFs?
* What are OCR limitations?
* How can OCR accuracy be improved?

## LLM / Groq

* Why Groq?
* What is LLM inference?
* What is temperature?
* What is a context window?
* How do you handle LLM failures?
* How do you validate structured LLM output?
* How do you reduce LLM costs?

## System Design

* How would you process 10,000 PDFs?
* How would you handle concurrent uploads?
* How would you scale the RAG system?
* How would you secure user documents?
* How would you monitor the system?
* How would you handle failed document processing?
* How would you reduce latency?

---

# 📚 Learning Objectives

By completing this project, you will gain practical experience with:

```text
Python
  ↓
FastAPI
  ↓
REST API Design
  ↓
PostgreSQL
  ↓
pgvector
  ↓
Embeddings
  ↓
OCR
  ↓
Document Processing
  ↓
LangChain
  ↓
RAG
  ↓
Groq LLM
  ↓
Structured Output
  ↓
Citations
  ↓
AI Evaluation
  ↓
Docker
  ↓
Production Architecture
```

---

# 🗺️ Development Roadmap

### Phase 1 — Infrastructure

* FastAPI
* Docker
* PostgreSQL
* pgvector

### Phase 2 — Database

* SQLAlchemy
* Alembic
* Database models

### Phase 3 — Document Upload

* PDF upload
* Validation
* Metadata

### Phase 4 — Document Processing

* PyMuPDF
* OCR
* Text cleaning

### Phase 5 — Chunking

* Chunking strategy
* Metadata preservation

### Phase 6 — Embeddings

* SentenceTransformers
* pgvector storage

### Phase 7 — Search

* Vector similarity
* Top-K retrieval

### Phase 8 — LLM

* Groq
* LangChain
* Prompt templates

### Phase 9 — RAG

* Retriever
* Context construction
* Answer generation

### Phase 10 — Citations

* Page-level sources
* Citation validation

### Phase 11 — Summarization

* Chunk summaries
* Hierarchical summarization

### Phase 12 — Structured Extraction

* JSON output
* Pydantic validation

### Phase 13 — Reports

* PDF report generation

### Phase 14 — Security

* JWT
* Authorization
* File security

### Phase 15 — Testing

* Unit tests
* API tests
* RAG tests

### Phase 16 — Evaluation

* Retrieval metrics
* Generation metrics
* Citation evaluation

### Phase 17 — Production

* Logging
* Error handling
* Docker optimization
* Background workers

### Phase 18 — Advanced RAG

* Hybrid search
* Reranking
* Query rewriting
* Multi-query retrieval

---

# 👨‍💻 Author

**Syed Jawad Ali**

Python Backend Developer | FastAPI | Django | Generative AI | LLM | RAG

---

# ⭐ Project Purpose

This project is built to demonstrate practical experience in:

**Backend Engineering + Generative AI + RAG + LLM Applications + Vector Search + Document Intelligence**

It is intentionally designed as a production-style learning project rather than a simple tutorial application.
