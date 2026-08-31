from langgraph.graph import StateGraph, END
from app.agents.state import RAGState
from app.agents.nodes import retrieve_node, answer_node


def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", answer_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
