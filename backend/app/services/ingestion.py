from typing import List
from app.services.chroma_service import get_chroma_client, get_collection


def ingest_chunks(chunks: List[dict]) -> None:
    client = get_chroma_client()
    collection = get_collection(client)

    ids        = [str(chunk["chunk_id"]) for chunk in chunks]
    documents  = [chunk["text"] for chunk in chunks]
    embeddings = [chunk["embedding"].tolist() for chunk in chunks]
    metadatas  = [{"page_number": chunk["page_number"]} for chunk in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks into ChromaDB")
    