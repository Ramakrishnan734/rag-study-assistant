# Prompt Engineering

## Goal
Improve the LLM prompt by separating system and user messages,
adding page citations, and preventing hallucination.

---

## File
`backend/app/rag/llm.py` — updated

---

## What Changed

### Before — single user message:
```python
messages=[
    {
        "role": "user",
        "content": "You are helpful... Context:... Question:..."
    }
]
```

### After — system + user messages:
```python
messages=[
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user", 
        "content": "Context:... Question:..."
    }
]
```

---

## SYSTEM_PROMPT

```python
SYSTEM_PROMPT = """You are an expert study assistant that helps 
students understand their study materials. 
Answer questions clearly and concisely.
Always cite the page number where you found the answer.
If the answer is not in the context, say "I don't know."
Never make up information that is not in the context."""
```

Defines:
- Who the LLM is
- How it should behave
- What format to use
- What to do when answer not found
- Hallucination prevention

---

## User Message Structure

```python
user_message = f"""Context:
{context}

Question: {query}

Please provide a clear answer with page citations."""
```

Three parts:
1. Context — retrieved chunks with page numbers
2. Question — user's query
3. Instruction — how to format the answer

---

## Key Concepts

| Concept | Explanation |
|---|---|
| System prompt | Sets LLM personality and rules |
| User message | Contains context and question |
| role: "system" | LLM reads as instructions |
| role: "user" | LLM reads as request |
| SYSTEM_PROMPT constant | Reused across all LLM calls |
| Page citations | LLM instructed to cite sources |
| "Never make up" | Explicit hallucination prevention |

---

## Why Two Message Roles?

LLM is trained to treat roles differently:

system → "this is how I should behave"
Sets personality, rules, format

user → "this is what I need to do"
Contains context and question


Mixing everything into one user message:
- Rules and content get mixed up
- LLM less focused on instructions
- Weaker, less structured answers

Separating into system + user:
- Rules clearly separated from request
- LLM follows instructions more reliably
- Cleaner, more professional answers ✅

---

## Why SYSTEM_PROMPT as a Constant?

```python
# ✅ constant — defined once, reused everywhere
SYSTEM_PROMPT = """..."""

def get_answer(chunks, query):
    ...
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        ...
    ]
```

Benefits:
- Easy to update in one place
- Consistent behavior across all calls
- Clean separation from business logic

---

## Before vs After Comparison

Query: "What does page 1 introduce?"

Before:

Answer: Page 1 introduces RAG systems.


After:

Answer: Page 1 introduces RAG (Retrieval-Augmented Generation)
systems.【Page 1】


Improvements:
- Full name expanded ✅
- Page citation added 【Page 1】 ✅
- More professional tone ✅
- Follows system prompt instructions ✅

---

## Hallucination Prevention

Three layers of protection:

Layer 1 — Retrieval:
Only relevant chunks sent to LLM
→ Less irrelevant information

Layer 2 — Prompt instruction:
"Answer using ONLY the context below"
→ LLM stays grounded in document

Layer 3 — System prompt:
"Never make up information"
→ Explicit instruction to not hallucinate


---

## Data Flow

chunks + query
        ↓
build_prompt()
    → context string from chunks
    → user_message with context + question
        ↓
get_answer()
    → messages = [system, user]
    → client.chat.completions.create()
        ↓
response.choices[0].message.content
        ↓
"RAG (Retrieval-Augmented Generation) systems.【Page 1】" ✅

---

## Test Result

Query: "What does page 1 introduce?"

Output:
"Page 1 introduces RAG (Retrieval-Augmented Generation) 
systems.【Page 1】"

Improvements confirmed:
- Full term expanded ✅
- Page citation present ✅
- Professional tone ✅
- No hallucination ✅

---

## What Comes Next

Milestone 10 — FastAPI Routes

Build API endpoints so frontend can talk to RAG pipeline:
- POST /upload — accepts PDF, runs ingestion pipeline
- POST /chat — accepts question, returns LLM answer

llm.py output
        ↓
FastAPI route
        ↓
JSON response to frontend
