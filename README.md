# AskMyPDF — RAG Study Assistant

> Upload any PDF. Ask questions. Get cited answers.

A production-style RAG (Retrieval-Augmented Generation) application built with FastAPI, LangGraph, and ChromaDB. Upload a PDF, ask natural language questions, and receive answers grounded in the document's content — with source citations.

---

## Architecture

PDF Upload
↓
PDF Processor (PyMuPDF)
↓
Chunker (recursive text splitting)
↓
Embedder (all-MiniLM-L6-v2 via Sentence Transformers)
↓
ChromaDB (local vector store)
↓
LangGraph Agent (retriever node → LLM node)
↓
Groq LLM (openai/gpt-oss-20b)
↓
FastAPI → React Frontend


**Key design decision:** LangGraph is used instead of a simple chain so the retrieval and generation steps are explicit, inspectable nodes in a state machine — making the system easier to extend with re-ranking, query rewriting, or multi-hop retrieval later.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Agent orchestration | LangGraph |
| Vector store | ChromaDB 1.5.9 |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| LLM | Groq (`openai/gpt-oss-20b`) |
| Frontend | React + Vite |
| Testing | pytest (27 passing tests) |
| Runtime | Python 3.12 |

---

## Features

- **PDF ingestion** — Upload any PDF; pages are extracted, cleaned, and chunked
- **Semantic search** — Queries are embedded and matched against document chunks using cosine similarity
- **Cited answers** — Responses reference the source chunks they were generated from
- **Streaming-ready FastAPI backend** — CORS configured, modular route structure
- **Health check endpoint** — `/health` for uptime monitoring

---

## Project Structure

rag-study-assistant/
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI app entry point
│ │ ├── config/settings.py # Environment config
│ │ ├── rag/
│ │ │ ├── pdf_processor.py # Page extraction + text cleaning
│ │ │ ├── chunker.py # Recursive text splitting
│ │ │ ├── embedder.py # Sentence Transformer embeddings
│ │ │ └── retriever.py # ChromaDB similarity search
│ │ ├── agents/
│ │ │ ├── state.py # LangGraph state schema
│ │ │ ├── nodes.py # Retriever + LLM nodes
│ │ │ └── rag_graph.py # Graph assembly
│ │ ├── services/
│ │ │ ├── ingestion.py # End-to-end PDF → ChromaDB pipeline
│ │ │ └── chroma_service.py
│ │ └── api/routes/
│ │ ├── health.py
│ │ ├── upload.py
│ │ └── chat.py
│ ├── tests/ # 27 pytest tests
│ └── requirements.txt
└── frontend/
└── src/ # React + Vite


---

## Local Setup

### Prerequisites
- Python 3.12
- Node.js 18+
- A [Groq API key](https://console.groq.com)

### Backend

```bash
git clone https://github.com/Ramakrishnan734/rag-study-assistant
cd rag-study-assistant/backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`
Health check: `http://localhost:8000/health`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### Run Tests

```bash
cd backend
pytest tests/ -v
# 27 tests passing
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Upload a PDF for ingestion |
| POST | `/chat` | Ask a question against the uploaded PDF |

---

## What I Learned Building This

- How RAG pipelines work end-to-end: chunking strategy directly affects retrieval quality
- Why LangGraph over plain chains: state machines make agent logic inspectable and extensible
- ChromaDB persistence and collection management
- FastAPI dependency injection pattern for clean route architecture
- Writing pytest fixtures for components that depend on embeddings and vector stores

---

## Roadmap

- [ ] Deploy to Render 
- [ ] Add re-ranking step (cross-encoder)
- [ ] Multi-PDF support
- [ ] Query rewriting node in LangGraph graph
- [ ] Response latency benchmarks

---

## Part of a Larger Roadmap

This is **Project 1** of a 7-phase Agentic AI learning roadmap (July 2026 → June 2027).

**Next:** Multi-Agent Research Assistant using CrewAI — input a topic, three agents research + synthesize + write → structured report.

---

## Author

**Ramakrishnan** — 3rd year CSE, SASTRA University  
[GitHub](https://github.com/Ramakrishnan734) · 
