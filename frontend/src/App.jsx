import { useState } from "react"

function App() {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState("")
  const [query, setQuery] = useState("")
  const [answer, setAnswer] = useState("")
  const [sources, setSources] = useState([])

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a PDF file first.")
      return
    }
    setStatus("Uploading...")
    const formData = new FormData()
    formData.append("file", file)
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData
      })
      const data = await response.json()
      setStatus(`✅ ${data.message} (${data.chunks_stored} chunks stored)`)
    } catch (error) {
      setStatus("❌ Upload failed. Is the backend running?")
    }
  }

  const handleAsk = async () => {
    if (!query) return
    setAnswer("Thinking...")
    setSources([])
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      })
      const data = await response.json()
      setAnswer(data.answer)
      setSources(data.sources)
    } catch (error) {
      setAnswer("❌ Chat failed. Is the backend running?")
    }
  }

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", padding: "0 20px", fontFamily: "sans-serif" }}>
      <h1>RAG Study Assistant</h1>
      <p>Upload a PDF and ask questions about it.</p>

      {/* Upload Section */}
      <div style={{ marginTop: "30px" }}>
        <h2>Upload PDF</h2>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload</button>
        {status && <p>{status}</p>}
      </div>

      {/* Chat Section */}
      <div style={{ marginTop: "40px" }}>
        <h2>Ask a Question</h2>
        <input
          type="text"
          placeholder="Type your question here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />
        <button onClick={handleAsk}>Ask</button>

        {answer && (
          <div style={{ marginTop: "20px" }}>
            <p><strong>Answer:</strong> {answer}</p>
            {sources.length > 0 && (
              <div style={{ marginTop: "10px" }}>
                <strong>Sources:</strong>
                {sources.map((s, i) => (
                  <p key={i} style={{ color: "#888", fontSize: "13px" }}>
                    Page {s.page_number}: {s.text}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App