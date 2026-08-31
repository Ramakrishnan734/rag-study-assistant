# ChromaDB Storage

## Goal
Store chunk text, embeddings, and metadata into ChromaDB so we can
search by similarity when a user asks a question.

---

## Files
- `backend/app/services/chroma_service.py` — connection and collection
- `backend/app/services/ingestion.py` — pipeline for storing chunks

---

## Functions

### get_chroma_client()
**Purpose:** Create and return a ChromaDB client that saves to disk.

```python
def get_chroma_client():
    client = chromadb.PersistentClient(path="chroma_db")
    return client
```

### get_collection(client)
**Purpose:** Get or create the "study_assistant" collection.

```python
def get_collection(client):
    collection = client.get_or_create_collection(name="study_assistant")
    return collection
```

### ingest_chunks(chunks: List[dict]) -> None
**Purpose:** Store all embedded chunks into ChromaDB.

**Steps:**
1. Get ChromaDB client and collection
2. Extract ids, documents, embeddings, metadatas as lists
3. Call collection.add() to store everything
4. Print confirmation message

---

## Key Concepts

| Concept | Explanation |
|---|---|
| Client | Connection to ChromaDB database |
| Collection | Like a table — holds all chunks |
| PersistentClient | Saves to disk — survives restart |
| EphemeralClient | Saves to memory — disappears on restart |
| get_or_create_collection() | Safe — never crashes if already exists |
| collection.add() | Stores ids, documents, embeddings, metadatas |
| str(chunk_id) | ChromaDB requires string IDs not integers |
| .tolist() | Converts NumPy array to Python list |

---

## Why Two Files?

Single Responsibility Principle:
chroma_service.py → only knows about ChromaDB
"How do I talk to ChromaDB?"

ingestion.py → only knows about the pipeline
"How do I store chunks?"


Benefits:
- Easy to debug — problem with DB? Look in chroma_service.py
- Easy to reuse — other files import only what they need
- Clean and readable — each file has one clear job

---

## What ChromaDB Stores

For each chunk, ChromaDB stores four things:

```python
collection.add(
    ids=["0", "1", "2"],          # unique string ID per chunk
    documents=["text...", ...],    # actual text content
    embeddings=[[0.23, ...], ...], # 384-dimensional vectors
    metadatas=[{"page_number": 1}] # extra info for citations
)
```

---

## Why PersistentClient?

```python
# PersistentClient — saves to disk ✅
client = chromadb.PersistentClient(path="chroma_db")
# Data survives after program stops

# EphemeralClient — saves to memory ❌
client = chromadb.EphemeralClient()
# Data disappears when program ends
```

We use PersistentClient so we don't re-process PDFs every time.

---

## Why get_or_create_collection()?

```python
# create_collection() — crashes if already exists ❌
client.create_collection(name="study_assistant")

# get_or_create_collection() — always safe ✅
client.get_or_create_collection(name="study_assistant")
```

First run → creates collection
Every run after → gets existing collection
Never crashes!

---

## Why .tolist()?

```python
# model.encode() returns NumPy array
embedding = model.encode("some text")
type(embedding)  # numpy.ndarray ❌ ChromaDB rejects this

# Convert to Python list
embedding.tolist()  # [0.23, 0.87, ...] ✅ ChromaDB accepts this
```

---

## Data Flow

embed_chunks() output — List[dict with embeddings]
            ↓
get_chroma_client() — connect to chroma_db/
            ↓
get_or_create_collection() — get "study_assistant"
            ↓
extract ids, documents, embeddings, metadatas
            ↓
collection.add() — store everything
            ↓
chroma_db/ on disk:
  ├── chroma.sqlite3        (metadata)
  └── 588e08de-.../         (vector data)

---

## Problem Encountered

ChromaDB 0.5.0 incompatible with NumPy 2.0:
- Error: np.float_ was removed in NumPy 2.0 release
- Solution: pip install --upgrade chromadb (0.5.0 → 1.5.9)
- Lesson: always check package version compatibility

---

## Test Result

Used the same 2-page synthetic PDF from Milestone 2.

Output:
Stored 2 chunks into ChromaDB ✅
chroma_db/ folder created:
- chroma.sqlite3 — metadata database
- 588e08de-.../ — vector data folder

Data persists on disk after program stops.

---

## What Comes Next

Milestone 6 — Retriever

Given a user question:
1. Embed the question → query vector
2. ChromaDB finds closest chunk vectors
3. Return most relevant chunks as context
4. LLM uses context to generate accurate answer

ingest_chunks() stored this:
[text, embedding, page_number] per chunk

retriever.py will search this:
question → embed → search → top K chunks → LLM context