import pytest
from app.rag.pdf_processor import clean_text, extract_pages

def test_clean_text_removes_extra_spaces():
    result = clean_text("hello   world")
    assert result == "hello world"

def test_clean_text_keeps_single_newline():
    result = clean_text("hello\nworld")
    assert result == "hello\nworld"

def test_clean_text_empty_string():
    result = clean_text("")
    assert result == ""

def test_extract_pages_returns_list():
    pages = extract_pages("../documents/test.pdf")
    assert isinstance(pages, list)

def test_extract_pages_has_required_keys():
    pages = extract_pages("../documents/test.pdf")
    assert len(pages) > 0
    for page in pages:
        assert "page_number" in page
        assert "text" in page
        assert "char_count" in page

def test_extract_pages_page_number_starts_at_1():
    pages = extract_pages("../documents/test.pdf")
    assert pages[0]["page_number"] == 1
