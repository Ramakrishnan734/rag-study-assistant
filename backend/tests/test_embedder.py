import pytest
from app.rag.embedder import embed_chunks

sample_chunks = [
    {"chunk_id": 0, "text": "This is a test chunk.", "page_number": 1},
    {"chunk_id": 1, "text": "Another test chunk here.", "page_number": 2}
]

def test_embed_chunks_returns_list():
    result = embed_chunks(sample_chunks)
    assert isinstance(result, list)

def test_embed_chunks_adds_embedding_key():
    result = embed_chunks(sample_chunks)
    for chunk in result:
        assert "embedding" in chunk

def test_embedding_has_correct_dimensions():
    result = embed_chunks(sample_chunks)
    for chunk in result:
        assert len(chunk["embedding"]) == 384

def test_embed_chunks_preserves_original_keys():
    result = embed_chunks(sample_chunks)
    for chunk in result:
        assert "chunk_id" in chunk
        assert "text" in chunk
        assert "page_number" in chunk
