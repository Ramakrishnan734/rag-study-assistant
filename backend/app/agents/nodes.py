from app.rag.retriever import retrieve_chunks
from app.rag.llm import get_answer
from app.agents.state import RAGState


def retrieve_node(state: RAGState) -> dict:
    query = state["query"]
    chunks = retrieve_chunks(query)
    return {"chunks": chunks}


def answer_node(state: RAGState) -> dict:
    query = state["query"]
    chunks = state["chunks"]
    answer = get_answer(chunks, query)
    return {"answer": answer}