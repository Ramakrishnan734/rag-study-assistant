from fastapi import APIRouter, HTTPException
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.agents.rag_graph import build_rag_graph

router = APIRouter()
graph = build_rag_graph()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = graph.invoke({
            "query": request.query,
            "chunks": [],
            "answer": ""
        })
        sources = [
            {"text": c["text"], "page_number": c["page_number"]}
            for c in result["chunks"]
        ]
        return ChatResponse(
            answer=result["answer"],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))