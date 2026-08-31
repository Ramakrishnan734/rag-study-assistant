from typing import List
from sentence_transformers import SentenceTransformer
from app.services.chroma_service import get_chroma_client, get_collection

model = SentenceTransformer('all-MiniLM-L6-v2')


def retrieve_chunks(query: str, top_k: int = 3) -> List[dict]:
    client = get_chroma_client()
    collection = get_collection(client)

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "page_number": results["metadatas"][0][i]["page_number"],
            "distance": results["distances"][0][i]
        })
    return chunks