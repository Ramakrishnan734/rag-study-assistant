# React Frontend

## Goal
Build a browser UI so students can upload PDFs and ask questions,
connected to the FastAPI backend.

---

## File
`frontend/src/App.jsx`

---

## Two Sections

### Upload Section
User selects a PDF file and clicks Upload.
Frontend sends file to POST /upload.
Status message shows result.

### Chat Section
User types a question and clicks Ask.
Frontend sends query to POST /chat.
Answer and sources displayed below.

---

## State Variables

```javascript
const [file, setFile] = useState(null)      // selected PDF file
const [status, setStatus] = useState("")    // upload status message
const [query, setQuery] = useState("")      // question being typed
const [answer, setAnswer] = useState("")    // LLM answer
const [sources, setSources] = useState([]) // page citations
```

Five state variables track everything that changes in the UI.

---

## handleUpload

```javascript
const handleUpload = async () => {
  const formData = new FormData()
  formData.append("file", file)
  const response = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData
  })
  const data = await response.json()
  setStatus(`✅ ${data.message} (${data.chunks_stored} chunks stored)`)
}
```

Wraps file in FormData → sends to /upload → updates status.

---

## handleAsk

```javascript
const handleAsk = async () => {
  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  })
  const data = await response.json()
  setAnswer(data.answer)
  setSources(data.sources)
}
```

Sends query as JSON → receives answer and sources → updates state.

---

## Key Concepts

| Concept | Explanation |
|---|---|
| useState | React hook to track changing values |
| fetch() | Built-in browser function to call APIs |
| FormData | Wraps files for multipart HTTP upload |
| JSON.stringify() | Converts JS object to JSON string |
| async/await | Waits for fetch before updating state |
| Conditional rendering | Only shows answer when it exists |

---

## Why Two Servers?

Vite (port 5173) — serves the React UI
FastAPI (port 8000) — handles API requests

Both must run simultaneously.
React fetches data from FastAPI via HTTP.

---

## Data Flow

User selects PDF
    ↓
handleUpload() → FormData → fetch POST /upload
    ↓
FastAPI → extract → chunk → embed → store
    ↓
setStatus("✅ uploaded") → UI updates

User types question
    ↓
handleAsk() → JSON → fetch POST /chat
    ↓
FastAPI → LangGraph → ChromaDB → Groq
    ↓
setAnswer() + setSources() → UI updates ✅

---

## Test Result

Upload: "PDF uploaded and stored successfully (2 chunks stored)" ✅
Query: "What does page 1 introduce?"
Answer: "Page 1 introduces RAG (Retrieval-Augmented Generation) systems 【Page 1】" ✅
Sources: Page 1 and Page 2 displayed correctly ✅

---

## What Comes Next

Milestone 12 — Final Polish & Deployment
- Clean up UI styling
- Deploy backend to Render/Railway
- Deploy frontend to Vercel/Netlify
- Share live URL