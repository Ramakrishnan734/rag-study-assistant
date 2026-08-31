# AI Development Log — RAG Study Assistant

---

## Milestone 2 — PDF Ingestion
**Date:** August 2026

### What Was Implemented
- Created `backend/app/rag/pdf_processor.py`
- Two functions: `clean_text()` and `extract_pages()`
- Tested with a synthetic 2-page PDF

### Files Changed
- `backend/app/rag/pdf_processor.py` — new file

### Architecture Decision
Used PyMuPDF (imported as `fitz`) for PDF parsing because:
- Fast C-based rendering engine under the hood
- Preserves page numbers accurately
- Returns page-level text which maps cleanly to our metadata structure

### How It Works
1. Validate the file path and extension
2. Open the PDF with `fitz.open()`
3. Loop through every page using 0-based index
4. Extract raw text with `page.get_text()`
5. Clean the text with `clean_text()` — removes extra newlines and spaces
6. Skip empty pages
7. Store `{ page_number, text, char_count }` per page
8. Return list of all pages

### Key Concepts Learned
- `import fitz` = importing PyMuPDF (historical naming quirk)
- Context manager (`with fitz.open() as doc`) ensures file is always closed
- 0-based page index converted to 1-based page number for human readability
- Defensive programming — validate inputs before processing
- Empty string is falsy in Python — `if cleaned:` skips blank pages
- Type hints (`str`, `List[dict]`) make code readable and self-documenting
- `re.sub()` for pattern matching and substitution
- `.strip()` for trimming edge whitespace

### Why Return List of Dicts?
Returning `{ page_number, text, char_count }` instead of just strings
keeps metadata attached to content. Page numbers are needed later
for citations — "Answer found on page 4."

### Test Performed
Created a synthetic 2-page PDF using PyMuPDF itself.
Verified correct output:
- Page numbers are 1-indexed
- Text is clean
- Char counts are accurate
- Empty pages are skipped

### Problems Encountered
- Python 3.14 incompatible with pymupdf==1.24.3
  - PyMuPDF had no pre-built binary for Python 3.14
  - Attempted to compile from source — failed
  - Solution: switched to Python 3.12 via Homebrew

### What Comes Next
Milestone 3 — Text Chunking
- Split each page's text into smaller overlapping chunks
- Each chunk will carry forward the page number as metadata
- Chunks are the unit that gets embedded and stored in ChromaDB

## Milestone 3 — Text Chunking
**Date:** August 2026

### What Was Implemented
- Created `backend/app/rag/chunker.py`
- One function: `chunk_pages()`
- Uses `RecursiveCharacterTextSplitter` from `langchain_text_splitters`
- Tested successfully with test.pdf

### Files Changed
- `backend/app/rag/chunker.py` — new file
- `backend/test_chunker.py` — test script

### Architecture Decision
Used LangChain's `RecursiveCharacterTextSplitter` instead of manual splitting because:
- Tries to split on `\n\n` first, then `\n`, then ` `, then characters
- Respects natural language boundaries
- Battle-tested and industry standard

### How It Works
1. Receive list of page dicts from `extract_pages()`
2. Create splitter with `chunk_size=500, chunk_overlap=100`
3. Loop through each page
4. Split page text using `splitter.split_text()`
5. Each chunk carries forward `page_number` for citations
6. Assign unique `chunk_id` starting from 0
7. Return list of chunk dicts

### Key Concepts Learned
- `chunk_size` — max characters per chunk
- `chunk_overlap` — repeated characters between consecutive chunks to preserve context at boundaries
- "Recursive" splitting — tries `\n\n` → `\n` → ` ` → characters in order
- Python uses `+=1` not `++` for incrementing
- Type hints `-> List[dict]` document what a function returns
- `..` in file paths means go up one folder level
- Small test PDF (36, 43 chars) produces 1 chunk per page — correct behavior since both are below chunk_size=500

### Why chunk_overlap?
Without overlap, sentences cut at boundaries lose meaning.
With overlap=100, next chunk repeats last 100 chars of previous chunk
so context is preserved across boundaries.

### Why chunk_id?
ChromaDB needs a unique ID for every piece it stores.
chunk_id starts at 0 and increments across all pages globally
so every chunk in the entire document has a unique identifier.

### Test Performed
Used the same 2-page synthetic PDF from Milestone 2.
Output:
- Total pages: 2
- Total chunks: 2
- Chunk 0 | Page 1 | 36 chars
- Chunk 1 | Page 2 | 43 chars

No splitting occurred because both pages are below chunk_size=500.
This is correct behavior — splitter only splits when needed.

### Also Fixed
Two bugs found in `pdf_processor.py` from Milestone 2:
- `page = page_index + 1` → fixed to `page = doc[page_index]`
- `if cleaned():` → fixed to `if cleaned:`

### What Comes Next
Milestone 4 — Embeddings
- Convert each chunk's text into a vector (list of numbers)
- Use Sentence Transformers (free, runs locally)
- Vectors capture semantic meaning of text
- These vectors get stored in ChromaDB for similarity search

## Milestone 4 — Embeddings
**Date:** August 2026

### What Was Implemented
- Created `backend/app/rag/embedder.py`
- One function: `embed_chunks()`
- Uses `sentence-transformers` library with `all-MiniLM-L6-v2` model
- Tested successfully with test.pdf

### Files Changed
- `backend/app/rag/embedder.py` — new file
- `backend/test_embedder.py` — test script

### Architecture Decision
Used Sentence Transformers (`all-MiniLM-L6-v2`) instead of OpenAI embeddings because:
- Completely free — runs locally on machine
- No API key needed for embeddings
- 384-dimensional vectors — fast and lightweight
- Good quality for RAG applications

### How It Works
1. Load `all-MiniLM-L6-v2` model once at module level
2. Receive list of chunk dicts from `chunk_pages()`
3. Extract all text fields into a list
4. Pass entire list to `model.encode()` at once — faster than one by one
5. Loop through chunks using `enumerate()` to get index
6. Add `embedding` field to each chunk dict
7. Return same chunks with embedding added

### Key Concepts Learned
- Sentence Transformers convert text into 384-dimensional vectors
- Similar meaning = similar vectors = close together in vector space
- `model.encode()` converts text → list of numbers
- Model loaded outside function — loads once, reused every call
- `enumerate()` gives both index and value in a loop
- 384 dimensions = 384 numbers per chunk representing its meaning
- First run downloads model (~90MB) from HuggingFace automatically

### Why Load Model Outside Function?
Loading inside function means model reloads every call → slow.
Loading outside means model loads once when file is imported → fast.
This is a standard Python performance pattern.

### Why encode() the whole list at once?
```python
# ✅ fast — one batch call
embeddings = model.encode(texts)

# ❌ slow — individual calls in loop
for text in texts:
    embedding = model.encode(text)
```
Batch encoding is significantly faster than encoding one by one.

### Why all-MiniLM-L6-v2?
- MiniLM = Mini Language Model (lightweight)
- L6 = 6 transformer layers
- v2 = version 2
- 384 dimensions = good balance of speed and quality
- Industry standard for RAG applications

### Test Performed
Used the same 2-page synthetic PDF from Milestone 2.
Output:
- Chunk 0 | Page 1 | Embedding size: 384
- First 5 values: [-0.09193111  0.05233684  0.06776175 -0.01383959 -0.14034474]
- Chunk 1 | Page 2 | Embedding size: 384
- First 5 values: [-0.03750971  0.0160002   0.00585755 -0.01798345  0.06345271]

Both chunks successfully converted to 384-dimensional vectors.

### What Comes Next
Milestone 5 — ChromaDB Storage
- Store chunk text + embeddings + metadata in ChromaDB
- ChromaDB enables similarity search
- Given a query embedding, find the closest chunk embeddings
- This is the core of RAG retrieval

## Milestone 5 — ChromaDB Storage
**Date:** August 2026

### What Was Implemented
- Created `backend/app/services/chroma_service.py`
- Created `backend/app/services/ingestion.py`
- Chunks with embeddings are now stored persistently in ChromaDB
- Tested successfully with test.pdf

### Files Changed
- `backend/app/services/chroma_service.py` — new file
- `backend/app/services/ingestion.py` — new file
- `backend/test_ingestion.py` — test script

### Architecture Decision
Split into two files following Single Responsibility principle:
- `chroma_service.py` — only manages ChromaDB connection and collection
- `ingestion.py` — only manages the pipeline of storing chunks

### How It Works
1. `get_chroma_client()` creates a PersistentClient pointing to chroma_db/
2. `get_or_create_collection()` creates or gets existing "study_assistant" collection
3. Extract ids, documents, embeddings, metadatas from chunks as lists
4. `collection.add()` stores everything into ChromaDB
5. Data persists on disk in chroma_db/ folder

### Key Concepts Learned
- ChromaDB Client — connection to the database
- ChromaDB Collection — like a table, holds all chunks
- PersistentClient — saves data to disk, survives program restart
- EphemeralClient — saves to memory only, disappears on restart
- get_or_create_collection() — safe method, never crashes if exists
- collection.add() needs ids, documents, embeddings, metadatas
- IDs must be strings in ChromaDB — use str(chunk["chunk_id"])
- embedding.tolist() — converts NumPy array to Python list for ChromaDB
- Single Responsibility — each file does one job only

### Why PersistentClient?
Data survives after program stops.
Next time program runs, chunks are already there.
No need to re-process the same PDF twice.

### Why get_or_create_collection()?
- First run → creates the collection
- Every run after → gets the existing one
- Never crashes with "already exists" error

### Why str(chunk_id)?
ChromaDB requires IDs to be strings not integers.
str(0) → "0", str(1) → "1" etc.

### Why .tolist()?
model.encode() returns NumPy array.
ChromaDB only accepts Python lists.
.tolist() converts NumPy array → Python list.

### Problem Encountered
ChromaDB 0.5.0 incompatible with NumPy 2.0:
- Error: np.float_ was removed in NumPy 2.0
- Solution: upgraded ChromaDB from 0.5.0 to 1.5.9
- Real world lesson: always check package version compatibility

### Test Performed
Used the same 2-page synthetic PDF from Milestone 2.
Output:
- Stored 2 chunks into ChromaDB ✅
- chroma_db/ folder created with:
  - chroma.sqlite3 — metadata database
  - 588e08de-.../ — vector data folder

### What Comes Next
Milestone 6 — Retriever
- Given a user question, embed it into a vector
- Search ChromaDB for closest chunk vectors
- Return most relevant chunks as context
- This is the core of RAG retrieval

## Milestone 6 — Retriever
**Date:** August 2026

### What Was Implemented
- Created `backend/app/rag/retriever.py`
- One function: `retrieve_chunks()`
- Converts user query into embedding and searches ChromaDB
- Returns top K most relevant chunks with distance scores
- Tested successfully with "What are RAG systems?"

### Files Changed
- `backend/app/rag/retriever.py` — new file
- `backend/test_retriever.py` — test script

### Architecture Decision
Used same `all-MiniLM-L6-v2` model for query embedding as chunk embedding.
This is critical — query and chunks must use the SAME model so their
vectors exist in the same vector space and can be compared correctly.

### How It Works
1. Receive user query string and top_k parameter
2. Load ChromaDB client and collection
3. Convert query to embedding using model.encode()
4. Call collection.query() with query embedding and n_results=top_k
5. Parse results — documents, metadatas, distances
6. Return list of dicts with text, page_number, distance

### Key Concepts Learned
- Similarity search — find chunks closest in meaning to the query
- Distance score — lower = more similar, higher = less similar
- query_embeddings wrapped in list — ChromaDB supports batch queries
- results["documents"][0] — [0] means first query's results
- [0][i] — outer [0] = first query, inner [i] = each chunk
- top_k — only retrieve most relevant chunks, not all
- Same model for embedding and retrieval — vectors must be in same space

### Why Same Model for Query and Chunks?
If chunks use model A and queries use model B:
- They produce vectors in DIFFERENT spaces
- Comparison is meaningless — like comparing km to pounds
- Must use identical model for both embedding and retrieval

### Why top_k = 3?
- Too few chunks → LLM lacks context → bad answers
- Too many chunks → too many tokens → expensive and confusing
- 3-5 chunks is the sweet spot for RAG applications

### Why distance and not similarity score?
ChromaDB returns L2 distance by default:
- Distance 0.0 = identical meaning
- Distance < 0.5 = very similar
- Distance > 1.5 = very different

### Test Performed
Query: "What are RAG systems?"
Output:
Result 1 — Text: "Introduction to RAG systems" | Distance: 0.2662
Result 2 — Text: "Embeddings convert text to vectors" | Distance: 1.8531

ChromaDB correctly ranked the RAG systems chunk as most relevant.
Low distance (0.2662) confirms strong semantic match.
High distance (1.8531) confirms second chunk is less relevant.

### What Comes Next
Milestone 7 — Groq LLM Integration
- Send retrieved chunks to Groq LLM as context
- LLM reads context and generates a natural language answer
- User gets a real answer with page citations