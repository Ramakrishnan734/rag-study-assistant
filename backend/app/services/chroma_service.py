import chromadb

def get_chroma_client():
    client = chromadb.PersistentClient(path="chroma_db")
    return client


def get_collection(client):
    collection = client.get_or_create_collection(name="study_assistant")
    return collection

