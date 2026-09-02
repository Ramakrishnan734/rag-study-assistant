from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from app.models.responses import UploadResponse
from app.rag.pdf_processor import extract_pages
from app.rag.chunker import chunk_pages
from app.rag.embedder import embed_chunks
from app.services.ingestion import ingest_chunks

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        pages = extract_pages(tmp_path)
        chunks = chunk_pages(pages)
        chunks = embed_chunks(chunks)
        ingest_chunks(chunks)
    finally:
        os.remove(tmp_path)

    return UploadResponse(
        message="PDF uploaded and stored successfully",
        chunks_stored=len(chunks)
    )