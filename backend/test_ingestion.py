from app.rag.pdf_processor import extract_pages
from app.rag.chunker import chunk_pages
from app.rag.embedder import embed_chunks
from app.services.ingestion import ingest_chunks

pages = extract_pages("../documents/test.pdf")
chunks = chunk_pages(pages)
embedded = embed_chunks(chunks)
ingest_chunks(embedded)

print("Done! Check chroma_db/ folder exists now.")