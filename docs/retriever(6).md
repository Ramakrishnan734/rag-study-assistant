# Retriever

## Goal
Convert a user's question into an embedding, search ChromaDB for the
most relevant chunks, and return them as context for the LLM.

---

## File
`backend/app/rag/retriever.py`

---

## Function

### retrieve_chunks(query: str, top_k: int = 3) -> List[dict]
**Purpose:** Take a user question and return the most relevant chunks
from ChromaDB using similarity search.

**Returns:**
```python
[
    {
        "text": "Introduction to RAG systems.",
        "page_number": 1,
        "distance": 0.2662
    },
    {
        "text": "Embeddings convert text to vectors.",
        "page_number": 2,
        "distance": 1.8531
    }
]
```

**Steps:**
1. Get ChromaDB client and collection
2. Convert query string to embedding using model.encode()
3. Call collection.query() with query embedding
4. Parse results into list of dicts
5. Return top K chunks sorted by distance

---

## Key Concepts

| Concept | Explanation |
|---|---|
| Similarity search | Find chunks closest in meaning to the query |
| Distance score | Lower = more similar, higher = less similar |
| top_k | Number of chunks to return — default 3 |
| query_embeddings | Wrapped in list — ChromaDB supports batch queries |
| results[0] | First query's results — we only send one query |
| Same model | Query and chunks must use identical model |

---

## Why Convert Query to Embedding?

ChromaDB stores chunks as vectors (embeddings).
To search by meaning, the query must also become a vector.

"What are RAG systems?"
↓
model.encode()
↓
[0.21, 0.85, 0.09, ...] ← query vector
↓
ChromaDB compares against all stored chunk vectors
↓
returns closest chunks by distance



---

## Why Same Model for Query and Chunks?

```python
# embedder.py — chunks
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunk_texts)

# retriever.py — queries
model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode(query)
```

If different models were used:
- Chunks exist in vector space A
- Query exists in vector space B
- Comparison is meaningless — like comparing km to pounds!

Same model = same vector space = valid comparison ✅

---

## Understanding Distance Scores

ChromaDB returns L2 distance by default: