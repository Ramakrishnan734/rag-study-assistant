import { useState } from "react"
import "./App.css"

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

  const isError = (text) => text.startsWith("❌")

  return (
    <div className="container">
      <div className="header">
        <h1>AskMyPDF</h1>
        <p>Upload a PDF and ask questions about it.</p>
      </div>

      {/* Upload Section */}
      <div className="card">
        <h2>Upload PDF</h2>
        <div className="upload-row">
          <label className="file-label">
            Choose File
            <input
              className="file-input"
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </label>
          <span className="file-name">
            {file ? file.name : "no file selected"}
          </span>
          <button className="btn btn-primary" onClick={handleUpload}>
            Upload
          </button>
        </div>
        {status && (
          <div className={`status ${isError(status) ? "error" : ""}`}>
            {status}
          </div>
        )}
      </div>

      {/* Chat Section */}
      <div className="card">
        <h2>Ask a Question</h2>
        <input
          className="input-field"
          type="text"
          placeholder="Type your question here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button className="btn btn-primary" onClick={handleAsk}>
          Ask
        </button>

        {answer && (
          <div className="answer-box">
            <div className="answer-label">Answer</div>
            <div className="answer-text">{answer}</div>

            {sources.length > 0 && (
              <div className="sources">
                <div className="sources-label">Sources</div>
                {sources.map((s, i) => (
                  <div key={i} className="source-item">
                    <div className="page-tag">Page {s.page_number}</div>
                    {s.text}
                  </div>
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
