# Text Chunking

## Goal
Split each page's text into smaller overlapping chunks and return
structured data that the embedder can use in the next step.

---

## File
`backend/app/rag/chunker.py`

---

## Function

### chunk_pages(pages: List[dict], chunk_size: int = 500, chunk_overlap: int = 100) -> List[dict]
**Purpose:** Take the list of page dicts from extract_pages() and split
each page's text into smaller chunks.

**Returns:**
```python
[
    { "chunk_id": 0, "text": "...", "page_number": 1 },
    { "chunk_id": 1, "text": "...", "page_number": 1 },
    { "chunk_id": 2, "text": "...", "page_number": 2 },
]
```

**Steps:**
1. Create RecursiveCharacterTextSplitter with chunk_size and chunk_overlap
2. Initialize empty chunks list and chunk_id = 0
3. Loop through each page dict
4. Split page["text"] using splitter.split_text()
5. For each split text, append chunk dict with chunk_id, text, page_number
6. Increment chunk_id by 1
7. Return chunks list

---

## Key Concepts

| Concept | Explanation |
|---|---|
| chunk_size | Max characters allowed in one chunk |
| chunk_overlap | Characters repeated between consecutive chunks |
| RecursiveCharacterTextSplitter | Splits on \n\n → \n → space → chars in order |
| chunk_id | Unique identifier for every chunk across all pages |
| page_number | Carried forward from page dict for citations |
| += 1 | Python's way to increment — no ++ operator |
| -> List[dict] | Return type hint — documents what function returns |

---

## Why Not Embed Whole Pages?

Embedding a whole page creates one vector that represents the
average meaning of everything on that page.

If a page covers 5 different concepts, the embedding is a weak
average of all 5. A user's question about concept 3 will match
poorly against that average embedding.

Smaller chunks = tighter meaning per embedding = better retrieval.

---

## Why chunk_overlap?

Without overlap:
