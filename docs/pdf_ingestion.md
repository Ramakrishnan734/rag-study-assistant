# PDF Ingestion

## Goal
Extract text from a PDF file, page by page, and return structured data
that the chunker can use in the next step.

---

## File
`backend/app/rag/pdf_processor.py`

---

## Functions

### clean_text(text: str) -> str
**Purpose:** Take raw messy PDF text and normalize it.

**What it fixes:**
- 3 or more newlines in a row → replaced with 2 newlines
- 2 or more spaces in a row → replaced with 1 space
- Leading/trailing whitespace → removed

**Tools used:**
- `re.sub()` — pattern matching and substitution
- `.strip()` — trim edges

**Example:**
input  → "Machine    learning\n\n\n\nis great"
output → "Machine learning\n\nis great"

---

### extract_pages(pdf_path: str) -> List[dict]
**Purpose:** Open a PDF and extract text from every page.

**Returns:**
```python
[
    { "page_number": 1, "text": "...", "char_count": 842 },
    { "page_number": 2, "text": "...", "char_count": 1203 },
]
```

**Steps:**
1. Convert path string to Path object
2. Validate — file must exist and must be a .pdf
3. Open PDF with fitz.open()
4. Loop through every page (0-based index)
5. Extract raw text with page.get_text()
6. Clean text with clean_text()
7. Skip empty pages
8. Append { page_number, text, char_count } to list
9. Return the list

---

## Key Concepts

| Concept | Explanation |
|---|---|
| import fitz | PyMuPDF's Python name — same library, historical naming |
| with fitz.open() | Context manager — auto closes file even if crash occurs |
| page_index + 1 | Convert 0-based (computer) to 1-based (human) page numbers |
| if cleaned: | Empty string is falsy — skips blank pages automatically |
| raise FileNotFoundError | Defensive programming — fail early with clear message |
| List[dict] | Type hint — documents what the function returns |
| len(cleaned) | Counts characters in the cleaned string |

---

## Why List of Dicts and Not Just Strings?

Storing page_number alongside text means citations work later.

Without metadata:
["page 1 text", "page 2 text"]
— we lose which page the text came from

With metadata:
[
    { "page_number": 1, "text": "...", "char_count": 842 },
    { "page_number": 2, "text": "...", "char_count": 1203 },
]
— page number travels with the text through the entire pipeline

Later the user sees:
Sources:
[1] page 1 — document.pdf
[2] page 3 — document.pdf

This is only possible because we attached page_number from the start.

---

## Data Flow

PDF file on disk
      ↓
validate path and extension
      ↓
fitz.open() — open the PDF
      ↓
loop each page (0, 1, 2 ... n)
      ↓
  page.get_text() — raw text
      ↓
  clean_text() — normalized text
      ↓
  skip if empty
      ↓
  { page_number, text, char_count }
      ↓
return List[dict]

---

## Libraries Used

| Library | Imported As | Purpose |
|---|---|---|
| PyMuPDF | fitz | Open and read PDF files |
| re | re | Pattern matching and text substitution |
| pathlib.Path | Path | Clean cross-platform file path handling |
| typing.List | List | Type hints for function signatures |

---

## Test Result

Created a 2-page synthetic PDF using PyMuPDF itself.

Output:
Page 1: 36 chars — "Page 1: Introduction to RAG systems."
Page 2: 43 chars — "Page 2: Embeddings convert text to vectors."

Both pages extracted correctly.
Page numbers are 1-indexed.
Text is clean.
Empty pages are skipped.

---

## Problem Encountered

Python 3.14 incompatible with pymupdf 1.24.3.
PyMuPDF had no pre-built binary for Python 3.14.
Attempted source compilation — failed.
Solution: switched to Python 3.12 via Homebrew.
This is a real-world engineering problem — package versions
lag behind new Python releases.

---

## What Comes Next

The list of page dicts goes into the chunker.

Each page's text is too long to embed as one piece.
We split it into smaller overlapping chunks.
Each chunk carries the page number forward so citations still work.

extract_pages() output
        ↓
chunker.py
        ↓
[
    { "chunk_id": 1, "text": "...", "page_number": 1 },
    { "chunk_id": 2, "text": "...", "page_number": 1 },
    { "chunk_id": 3, "text": "...", "page_number": 2 },
]