from app.rag.retriever import retrieve_chunks

query = "What are RAG systems?"
chunks = retrieve_chunks(query, top_k=2)

print(f"Query: {query}")
print(f"Found {len(chunks)} chunks")
print()

for i, chunk in enumerate(chunks):
    print(f"Result {i+1}")
    print(f"Text: {chunk['text']}")
    print(f"Page: {chunk['page_number']}")
    print(f"Distance: {chunk['distance']:.4f}")
    print()