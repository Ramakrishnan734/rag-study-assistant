from app.agents.rag_graph import build_rag_graph

graph = build_rag_graph()

result = graph.invoke({
    "query": "What does page 1 introduce?",
    "chunks": [],
    "answer": ""
})

print(f"Question: {result['query']}")
print(f"Answer: {result['answer']}")