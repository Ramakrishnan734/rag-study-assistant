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