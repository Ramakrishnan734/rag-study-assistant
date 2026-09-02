import pytest
from app.rag.chunker import chunk_pages

sample_pages = [
    {"page_number": 1, "text": "This is a sample text for testing the chunker. " * 20, "char_count": 500},
    {"page_number": 2, "text": "Another page with some content. " * 20, "char_count": 500}
]

def test_chunk_pages_returns_list():
    chunks = chunk_pages(sample_pages)
    assert isinstance(chunks, list)

def test_chunk_pages_not_empty():
    chunks = chunk_pages(sample_pages)
    assert len(chunks) > 0

def test_chunk_has_required_keys():
    chunks = chunk_pages(sample_pages)
    for chunk in chunks:
        assert "chunk_id" in chunk
        assert "text" in chunk
        assert "page_number" in chunk

def test_chunk_id_starts_at_zero():
    chunks = chunk_pages(sample_pages)
    assert chunks[0]["chunk_id"] == 0

def test_chunk_text_not_empty():
    chunks = chunk_pages(sample_pages)
    for chunk in chunks:
        assert len(chunk["text"]) > 0

def test_chunk_page_number_valid():
    chunks = chunk_pages(sample_pages)
    for chunk in chunks:
        assert chunk["page_number"] in [1, 2]
