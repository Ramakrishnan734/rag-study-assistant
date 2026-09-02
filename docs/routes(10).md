# FastAPI Routes

## Goal
Build API endpoints so the frontend can talk to the RAG pipeline.
Three endpoints: health check, PDF upload, and chat.

---

## Files
- `backend/app/models/requests.py` — new file
- `backend/app/models/responses.py` — new file
- `backend/app/api/routes/health.py` — new file
- `backend/app/api/routes/upload.py` — new file
- `backend/app/api/routes/chat.py` — new file
- `backend/app/main.py` — updated

---

## Endpoints

| Method | Route | Receives | Returns |
|---|---|---|---|
| GET | /health | nothing | {"status": "ok"} |
| POST | /upload | PDF file | {"message": "...", "chunks_stored": N} |
| POST | /chat | {"query": "..."} | {"answer": "...", "sources": [...]} |

---

## Request Models

```python
# requests.py
class ChatRequest(BaseModel):
    query: str
```

Only /chat needs a request model.
/upload uses FastAPI's built-in UploadFile class.
/health receives nothing.

---

## Response Models

```python
# responses.py
class HealthResponse(BaseModel):
    status: str

class UploadResponse(BaseModel):
    message: str
    chunks_stored: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
```

BaseModel — Pydantic class for data shapes.
FastAPI validates response against model automatically.

---

## Route Structure

```python
# health.py
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")
```

```python
# upload.py
@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    # save to tempfile
    # extract → chunk → embed → ingest
    # delete tempfile
    return UploadResponse(message="...", chunks_stored=N)
```

```python
# chat.py
graph = build_rag_graph()  # built once at module level

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = graph.invoke({
        "query": request.query,
        "chunks": [],
        "answer": ""
    })
    return ChatResponse(answer=result["answer"], sources=sources)
```

---

## Registering Routers in main.py

```python
from app.api.routes import health, upload, chat

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(chat.router)
```

FastAPI app created once in main.py.
Each route file owns its own APIRouter.
main.py stays clean — no route logic inside it.

---

## Key Concepts

| Concept | Explanation |
|---|---|
| APIRouter | Mini router for one group of routes |
| BaseModel | Pydantic class for data shapes |
| BaseSettings vs BaseModel | Config vs data shapes |
| UploadFile | FastAPI's special class for file uploads |
| tempfile | Temporary file deleted after processing |
| app.include_router() | Registers router into main app |
| response_model | FastAPI validates and documents response |
| Graph at module level | Built once, reused every request |

---

## Why APIRouter Instead of FastAPI?

FastAPI() creates the whole application — done once in main.py.
APIRouter() creates a mini router for one group of routes.

CEO analogy:
- FastAPI app = CEO — runs the whole company
- APIRouter = department — handles its own work
- include_router() = CEO delegates to department ✅

---

## Why tempfile?

Once PDF is processed and stored in ChromaDB, the file is no longer needed.
tempfile creates a temporary file deleted after processing.
No storage wasted. Cleanup always happens via finally block.

```python
with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
    contents = await file.read()
    tmp.write(contents)
    tmp_path = tmp.name

try:
    pages = extract_pages(tmp_path)
    ...
finally:
    os.remove(tmp_path)  # always runs, even if error occurs
```

---

## Why Graph Built at Module Level?

```python
# ✅ built once — reused every request
graph = build_rag_graph()

# ❌ rebuilt every request — slow
@router.post("/chat")
async def chat(request):
    graph = build_rag_graph()
```

Same reason model loaded at module level in embedder.py and retriever.py.
Build once, reuse many times. ✅

---

## Data Flow

### Upload
PDF file
    ↓
extract_pages()    — PyMuPDF
    ↓
chunk_pages()      — RecursiveCharacterTextSplitter
    ↓
embed_chunks()     — Sentence Transformers
    ↓
ingest_chunks()    — ChromaDB storage
    ↓
UploadResponse(message, chunks_stored) ✅

### Chat
query string
    ↓
graph.invoke()
    ↓
retrieve_node — ChromaDB similarity search
    ↓
answer_node — Groq LLM
    ↓
ChatResponse(answer, sources) ✅

---

## Test Results

GET /health → {"status": "ok"} ✅
POST /upload → {"message": "PDF uploaded and stored successfully", "chunks_stored": 2} ✅
POST /chat → {"answer": "Page 1 introduces RAG (Retrieval-Augmented Generation) systems.【Page 1】", "sources": [...]} ✅

Tested via Swagger UI at http://localhost:8000/docs ✅

---

## What Comes Next

Milestone 11 — React Frontend

Build a browser UI so students can:
- Upload their PDF study material
- Type questions and get cited answers

FastAPI backend
    ↓
React frontend
    ↓
Student interacts via browser ✅