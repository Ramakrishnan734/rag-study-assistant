from app.rag.pdf_processor import extract_pages
from app.rag.chunker import chunk_pages
from app.rag.embedder import embed_chunks

pages = extract_pages("../documents/test.pdf")
chunks = chunk_pages(pages)
embedded = embed_chunks(chunks)

for chunk in embedded:
    print(f"Chunk {chunk['chunk_id']} | Page {chunk['page_number']}")
    print(f"Text: {chunk['text']}")
    print(f"Embedding size: {len(chunk['embedding'])}")
    print(f"First 5 values: {chunk['embedding'][:5]}")
    print()