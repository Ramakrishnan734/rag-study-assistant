import pytest
from app.rag.retriever import retrieve_chunks

def test_retrieve_chunks_returns_list():
    result = retrieve_chunks("What is RAG?")
    assert isinstance(result, list)

def test_retrieve_chunks_has_required_keys():
    result = retrieve_chunks("What is RAG?")
    for chunk in result:
        assert "text" in chunk
        assert "page_number" in chunk
        assert "distance" in chunk

def test_retrieve_chunks_respects_top_k():
    result = retrieve_chunks("What is RAG?", top_k=2)
    assert len(result) <= 2

def test_retrieve_chunks_text_not_empty():
    result = retrieve_chunks("What is RAG?")
    for chunk in result:
        assert len(chunk["text"]) > 0

def test_retrieve_chunks_distance_is_float():
    result = retrieve_chunks("What is RAG?")
    for chunk in result:
        assert isinstance(chunk["distance"], float)
