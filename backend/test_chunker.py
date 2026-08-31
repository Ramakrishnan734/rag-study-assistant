from app.rag.pdf_processor import extract_pages
from app.rag.chunker import chunk_pages

# Use the same test PDF from Milestone 2
pages = extract_pages("../documents/test.pdf")
chunks = chunk_pages(pages)

print(f"Total pages: {len(pages)}")
print(f"Total chunks: {len(chunks)}")
print()

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']} | Page {chunk['page_number']} | {len(chunk['text'])} chars")
    print(f"Text: {chunk['text'][:80]}...")
    print()