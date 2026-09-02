# LangGraph Agent

## Goal
Orchestrate the entire RAG pipeline as a stateful graph agent
with modular nodes connected by edges.

---

## Files
- `backend/app/agents/state.py` — defines state structure
- `backend/app/agents/nodes.py` — defines each step
- `backend/app/agents/rag_graph.py` — connects everything

---

## Graph Structure
START
↓
retrieve node — retrieve_chunks()
↓
generate node — get_answer()
↓
END


---

## state.py

### RAGState
Defines what data flows through the entire graph.

```python
class RAGState(TypedDict):
    query: str          # user's question
    chunks: List[dict]  # retrieved from ChromaDB
    answer: str         # LLM's final response
```

Think of state like a baton in a relay race:
- Passed between every node
- Each node reads from it and adds to it
- Carries all data from start to finish

---

## nodes.py

### retrieve_node(state: RAGState) -> dict
Reads query from state, retrieves relevant chunks from ChromaDB.

```python
def retrieve_node(state: RAGState) -> dict:
    query = state["query"]
    chunks = retrieve_chunks(query)
    return {"chunks": chunks}
```

### answer_node(state: RAGState) -> dict
Reads query and chunks from state, generates LLM answer.

```python
def answer_node(state: RAGState) -> dict:
    query = state["query"]
    chunks = state["chunks"]
    answer = get_answer(chunks, query)
    return {"answer": answer}
```

### Why Partial State Returns?
Each node returns only what it changed:
```python
# retrieve_node only updates chunks
return {"chunks": chunks}

# LangGraph merges automatically:
# {"query": "...", "chunks": [...], "answer": ""}
#   ↑ kept          ↑ updated        ↑ kept
```

No risk of accidentally overwriting other fields! ✅

---

## rag_graph.py

### build_rag_graph()
Connects nodes into a compiled runnable graph.

```python
def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", answer_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
```

---

## Key Concepts

| Concept | Explanation |
|---|---|
| StateGraph | LangGraph's main graph class |
| TypedDict | Structured dict — enforces field types |
| Node | One modular step in the graph |
| Edge | Connection between two nodes |
| END | Marks where graph stops |
| set_entry_point() | Defines first node to run |
| compile() | Validates and locks graph |
| invoke() | Runs compiled graph with initial state |

---

## Why LangGraph vs Simple Functions?

Simple function chain:
```python
# rigid, linear, no flexibility
chunks = retrieve_chunks(query)
answer = get_answer(chunks, query)
# if something fails — whole script crashes
# hard to extend or modify
```

LangGraph agent:
```python
# flexible, stateful, modular
result = graph.invoke({"query": query, ...})
# each step is isolated
# easy to add new nodes
# handles errors gracefully
# production ready ✅
```

---

## How invoke() Works

```python
result = graph.invoke({
    "query": "What does page 1 introduce?",
    "chunks": [],
    "answer": ""
})
```

Step 1 — retrieve node runs:

state = {"query": "What does page 1 introduce?", "chunks": [], "answer": ""}
retrieve_node returns {"chunks": [...]}
state = {"query": "...", "chunks": [...], "answer": ""}


Step 2 — generate node runs:

answer_node returns {"answer": "Page 1 introduces RAG systems."}
state = {"query": "...", "chunks": [...], "answer": "Page 1 introduces RAG systems."}


Step 3 — END reached → return final state ✅

---

## Problems Encountered

### 1. Node name conflicts with state key

ValueError: 'answer' is already being used as a state key

Node named "answer" conflicts with RAGState field "answer".
Solution: renamed node to "generate" ✅

### 2. Circular import
nodes.py accidentally imported from itself.
Solution: fixed import to point to state.py ✅

### 3. File not saving
Old code persisted despite editing in editor.
Solution: used terminal to overwrite file directly ✅

---

## Data Flow

graph.invoke({"query": "What does page 1 introduce?"})
        ↓
retrieve node
    → retrieve_chunks(query)
    → returns {"chunks": [...]}
        ↓
generate node
    → get_answer(chunks, query)
    → returns {"answer": "Page 1 introduces RAG systems."}
        ↓
END
        ↓
final state = {
    "query": "What does page 1 introduce?",
    "chunks": [...],
    "answer": "Page 1 introduces RAG systems."
}

---

## Libraries Used

| Library | Purpose |
|---|---|
| langgraph.graph | StateGraph, END |
| typing_extensions | TypedDict |
| typing | List |

---

## Test Result

Query: "What does page 1 introduce?"
Answer: "Page 1 introduces RAG systems." ✅

Full pipeline running through LangGraph agent successfully.

---

## What Comes Next

Milestone 9 — Prompt Engineering
- Improve prompt for better answers
- Add system message
- Handle edge cases — no chunks found, empty query
- Make answers more detailed and citation-aware

