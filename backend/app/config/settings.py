from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM - Groq
    groq_api_key: str
    groq_model: str = "llama3-8b-8192"

    # Embeddings - local, free
    embedding_model: str = "all-MiniLM-L6-v2"

    # ChromaDB
    chroma_db_path: str = "./chroma_db"
    chroma_collection_name: str = "documents"

    # Upload
    max_upload_size_mb: int = 50
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"


settings = Settings()
