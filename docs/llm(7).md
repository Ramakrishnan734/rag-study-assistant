# LLM Integration

## Goal
Build a prompt from retrieved chunks and user query, send it to
Groq LLM, and return a grounded natural language answer.

---

## File
`backend/app/rag/llm.py`

---

## Functions

### build_prompt(chunks: List[dict], query: str) -> str
**Purpose:** Combine retrieved chunks and user question into
one prompt string for the LLM.

**Example output:**

You are a helpful study assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
Page 1: Introduction to RAG systems.
Page 2: Embeddings convert text to vectors.

Question: What does page 1 introduce?

Answer:


**Steps:**
1. Loop through chunks
2. Build context string with page number and text
3. Insert context and query into prompt template
4. Return complete prompt string

---

### get_answer(chunks: List[dict], query: str) -> str
**Purpose:** Send prompt to Groq LLM and return the answer.

**Steps:**
1. Call build_prompt() to get prompt string
2. Send to Groq via client.chat.completions.create()
3. Extract answer from response.choices[0].message.content
4. Return answer as plain string

---

## Key Concepts

| Concept | Explanation |
|---|---|
| Prompt | Combined string of context + question sent to LLM |
| Context | Retrieved chunks formatted with page numbers |
| Hallucination | LLM confidently making up wrong answers |
| "ONLY context" | Forces LLM to stay grounded in document |
| client.chat.completions.create() | Sends message to Groq LLM |
| messages | List of role/content dicts — conversation history |
| role: "user" | This message is from the user |
| response.choices[0] | First response from LLM |
| .message.content | Actual answer text string |

---

## Why "Answer ONLY from context"?

Without this instruction:

LLM uses own training data
→ Could be outdated
→ Could hallucinate
→ Not from your document
→ Defeats purpose of RAG ❌


With this instruction:

LLM reads only provided chunks
→ Grounded in your document
→ Says "I don't know" when unsure
→ Trustworthy answers ✅


---

## Prompt Structure

[System instruction]
You are a helpful study assistant.
Answer using ONLY the context below.
If not in context, say "I don't know."

[Context from retrieved chunks]
Page 1: chunk text here...
Page 2: chunk text here...

[User question]
Question: What are RAG systems?

[LLM fills this in]
Answer:


---

## Why Two Functions?

```python
# build_prompt() — only builds the string
# Can be tested independently
# Can be modified without touching LLM code

# get_answer() — only talks to Groq
# Can swap LLM provider without touching prompt logic
# Each has one clear job — Single Responsibility ✅
```

---

## Groq Client Setup

```python
settings = Settings()
client = Groq(api_key=settings.groq_api_key)
```

Client is created once at module level — reused for every request.
API key comes from .env file via Settings — never hardcoded.

---

## Response Parsing

```python
response.choices[0].message.content
```

Unwrapping the response object:

response
.choices # list of possible responses
[0] # first response
.message # message object
.content # actual text string ✅


Groq can return multiple choices — we always take the first one.

---

## Data Flow

chunks + query
        ↓
build_prompt() → prompt string
        ↓
client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": prompt}]
)
        ↓
response object
        ↓
response.choices[0].message.content
        ↓
"RAG systems." ✅

---

## Problems Encountered

### 1. Settings Case Mismatch
```python
settings.GROQ_API_KEY  # ❌ AttributeError
settings.groq_api_key  # ✅ correct — pydantic uses lowercase
```

### 2. Model Decommissioned

llama3-8b-8192 → decommissioned by Groq
llama-3.1-8b-instant → not found
openai/gpt-oss-20b → ✅ working


Listed available models via:
```python
[m.id for m in client.models.list().data]
```

Always check available models when getting model errors!

---

## Libraries Used

| Library | Purpose |
|---|---|
| groq | Groq Python client — sends prompts to LLM |
| app.config.settings | Read API key and model name from .env |
| typing.List | Type hints |

---

## Test Result

Query: "What does page 1 introduce?"
Answer: "RAG systems." ✅

Query: "What are RAG systems?"
Answer: "I don't know." ✅ (correct — context too thin)

LLM correctly grounded in document context.
Hallucination prevention working as expected.

---

## What Comes Next

Milestone 8 — LangGraph Agent

All RAG components built so far:
- extract_pages() ✅
- chunk_pages() ✅
- embed_chunks() ✅
- ingest_chunks() ✅
- retrieve_chunks() ✅
- get_answer() ✅

LangGraph will orchestrate these into one intelligent agent:
retrieve → answer → respond
with state management and error handling.