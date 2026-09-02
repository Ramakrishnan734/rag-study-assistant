from pydantic import BaseModel
from typing import List

class HealthResponse(BaseModel):
    status: str

class UploadResponse(BaseModel):
    message: str
    chunks_stored: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]