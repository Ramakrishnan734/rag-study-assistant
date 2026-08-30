import re
from pathlib import Path
from typing import List

import fitz  # PyMuPDF


def clean_text(text: str) -> str:
    """Remove excessive whitespace and fix common PDF artifacts."""
    # Replace multiple newlines with a single one
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' {2,}', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


def extract_pages(pdf_path: str) -> List[dict]:
    """
    Open a PDF and extract text from every page.

    Returns a list of dicts, one per page:
    {
        "page_number": int,   # 1-indexed
        "text": str,          # cleaned text
        "char_count": int     # number of characters
    }
    """
    path=Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"not found {pdf_path}")
    if path.suffix.lower()!=".pdf":
        raise ValueError(f" file is not a PDF {pdf_path}")
    pages=[]

    with fitz.open(pdf_path) as doc:
        for page_index in range(len(doc)):
            page= page_index+1
            raw_text = page.get_text()
            cleaned= clean_text(raw_text)

            if cleaned():
                pages.append({
                    "page_number":page_index+1,
                    "text":cleaned,
                    "char_count":len(cleaned)
                })
    return pages