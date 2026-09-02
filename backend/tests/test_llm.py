import pytest
from app.rag.llm import build_prompt, get_answer

sample_chunks = [
    {"text": "RAG stands for Retrieval-Augmented Generation.", "page_number": 1, "distance": 0.25},
    {"text": "It combines retrieval and generation steps.", "page_number": 2, "distance": 0.30}
]

def test_build_prompt_returns_string():
    result = build_prompt(sample_chunks, "What is RAG?")
    assert isinstance(result, str)

def test_build_prompt_contains_query():
    result = build_prompt(sample_chunks, "What is RAG?")
    assert "What is RAG?" in result

def test_build_prompt_contains_chunk_text():
    result = build_prompt(sample_chunks, "What is RAG?")
    assert "RAG stands for Retrieval-Augmented Generation." in result

def test_build_prompt_contains_page_number():
    result = build_prompt(sample_chunks, "What is RAG?")
    assert "Page 1" in result

def test_get_answer_returns_string():
    result = get_answer(sample_chunks, "What is RAG?")
    assert isinstance(result, str)

def test_get_answer_not_empty():
    result = get_answer(sample_chunks, "What is RAG?")
    assert len(result) > 0
