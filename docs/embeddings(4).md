# Embeddings

## Goal
Convert each chunk's text into a vector (list of numbers) that captures
its semantic meaning, so ChromaDB can search by similarity later.

---

## File
`backend/app/rag/embedder.py`

---

## Function

### embed_chunks(chunks: List[dict]) -> List[dict]
**Purpose:** Take the list of chunk dicts from chunk_pages() and add
an embedding vector to each chunk.

**Returns:**
```python
[
    { 
        "chunk_id": 0, 
        "text": "Neural networks...", 
        "page_number": 1,
        "embedding": [0.23, 0.87, 0.11, ...] # 384 numbers
    },
]
```

**Steps:**
1. Extract all text fields into a list
2. Pass entire list to model.encode() in one batch
3. Loop through chunks using enumerate() to get index
4. Add embedding field to each chunk dict
5. Return same chunks with embedding added

---

## Key Concepts

| Concept | Explanation |
|---|---|
| SentenceTransformer | Class that loads and runs the embedding model |
| all-MiniLM-L6-v2 | Model name — lightweight, 384 dimensions |
| model.encode() | Converts text → vector (list of numbers) |
| 384 dimensions | Each text becomes 384 numbers representing meaning |
| enumerate() | Gives both index i and value in a loop |
| model at module level | Loads once when file is imported — not per call |
| batch encoding | Pass all texts at once — faster than one by one |

---

## What is an Embedding?

Raw text:
"Neural networks learn by adjusting weights"

After embedding:
[0.23, 0.87, 0.11, 0.45, -0.32, 0.67, ...] ← 384 numbers total

These numbers represent the MEANING of the text in 384-dimensional
vector space. Similar meanings = similar numbers = close vectors.

Example:
Dogs are great pets" → [0.23, 0.87, 0.11, ...]
"Canines make wonderful" → [0.24, 0.85, 0.12, ...]
↑ very close numbers!

"Quantum physics theory" → [0.91, 0.12, 0.78, ...]
↑ very different numbers!


---

## Why Not Use Whole Pages?

Embedding a whole page creates one vector representing the average
meaning of everything on that page.

If a page covers 5 concepts, the embedding is a weak average of all 5.
A question about concept 3 matches poorly against that average.

Smaller chunks = tighter meaning per embedding = better retrieval.

---

## Why Load Model Outside Function?

```python
# ✅ correct — loads ONCE when file is imported
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    ...

# ❌ wrong — reloads model every function call → slow!
def embed_chunks(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    ...
```

Model loading takes time. Load once, reuse forever.

---

## Why Batch Encode?

```python
# ✅ fast — one batch call
texts = [chunk["text"] for chunk in chunks]
embeddings = model.encode(texts)

# ❌ slow — individual calls in loop
for chunk in chunks:
    embedding = model.encode(chunk["text"])
```

Batch encoding processes all texts together — significantly faster.

---

## Why enumerate()?

```python
# Without enumerate — no index available
for chunk in chunks:
    chunk["embedding"] = embeddings[???]  # ❌ can't match!

# With enumerate — index available
for i, chunk in enumerate(chunks):
    chunk["embedding"] = embeddings[i]   # ✅ perfect match!
```

enumerate() gives both position (i) and value (chunk) simultaneously.

---

## Why all-MiniLM-L6-v2?

| Term | Meaning |
|---|---|
| MiniLM | Mini Language Model — lightweight |
| L6 | 6 transformer layers |
| v2 | Version 2 |
| 384 | Output dimensions |

Good balance of speed and quality.
Industry standard for RAG applications.
Free and runs locally — no API key needed.

---

## Model Download

First run downloads ~90MB from HuggingFace automatically.
Cached locally after first download — no re-download needed.

Warning shown on first run:
"You are sending unauthenticated requests to the HF Hub"
This is harmless — model still downloads correctly.

---

## Data Flow

List of chunk dicts from chunk_pages()
            ↓
Extract all text fields into list
            ↓
model.encode(texts) — batch encode all at once
            ↓
embeddings = [[0.23, 0.87, ...], [0.91, 0.12, ...], ...]
            ↓
enumerate(chunks) — loop with index
            ↓
chunk["embedding"] = embeddings[i]
            ↓
return List[dict] with embedding added

---

## Libraries Used

| Library | Imported As | Purpose |
|---|---|---|
| sentence_transformers | SentenceTransformer | Load and run embedding model |
| typing.List | List | Type hints for function signatures |

---

## Test Result

Used the same 2-page synthetic PDF from Milestone 2.

Output:
Chunk 0 | Page 1
Text: Page 1: Introduction to RAG systems.
Embedding size: 384
First 5 values: [-0.09193111  0.05233684  0.06776175 -0.01383959 -0.14034474]

Chunk 1 | Page 2
Text: Page 2: Embeddings convert text to vectors.
Embedding size: 384
First 5 values: [-0.03750971  0.0160002   0.00585755 -0.01798345  0.06345271]

Both chunks successfully converted to 384-dimensional vectors.

---

## What Comes Next

The embedded chunks go into ChromaDB for storage.

embed_chunks() output
        ↓
chroma_service.py
        ↓
ChromaDB stores:
- text (for retrieval)
- embedding (for similarity search)
- metadata: chunk_id, page_number (for citations)

When user asks a question:
1. Question gets embedded → query vector
2. ChromaDB finds closest chunk vectors → most relevant chunks
3. Those chunks go to the LLM as context → accurate answer