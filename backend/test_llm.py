from app.rag.retriever import retrieve_chunks
from app.rag.llm import get_answer

query = "What does page 1 introduce?"

chunks = retrieve_chunks(query, top_k=2)
answer = get_answer(chunks, query)

print(f"Question: {query}")
print()
print(f"Answer: {answer}")