import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [video, setVideo] = useState(null);
  const [language, setLanguage] = useState("Telugu");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setVideo(e.target.files[0]);
    setResult(null); // Clear previous results
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleUpload = async () => {
    if (!video) {
      alert("Please select a video file");
      return;
    }

    setIsLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("video", video);
    formData.append("language", language);

    try {
      const response = await axios.post(
        "https://nandakumar-9-ai-video-summarizer-backend.hf.space/upload",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Upload failed. Please check if the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>AI Video Summarizer + Quiz Generator</h1>
      </header>

      <main>
        <section className="upload-section">
          <div className="controls">
            <input 
              type="file" 
              accept="video/*"
              onChange={handleFileChange} 
            />
            
            <div className="language-selector">
              <label htmlFor="language-select" style={{ marginRight: '10px', fontWeight: 'bold' }}>
                Target Translation Language:
              </label>
              <select 
                id="language-select"
                value={language} 
                onChange={handleLanguageChange}
              >
                <option value="Telugu">Telugu</option>
                <option value="Hindi">Hindi</option>
                <option value="Tamil">Tamil</option>
                <option value="Kannada">Kannada</option>
                <option value="Malayalam">Malayalam</option>
                <option value="English">English</option>
              </select>
            </div>

            <button 
              onClick={handleUpload} 
              disabled={isLoading || !video}
            >
              {isLoading ? "Processing..." : "Upload & Generate"}
            </button>
          </div>
        </section>

        {isLoading && (
          <div className="loader-container">
            <div className="spinner"></div>
            <p className="loading-text">Processing video... This may take a minute.</p>
            <p className="loading-text" style={{ fontSize: '0.8rem' }}>Generating transcript, summary, translation, and quiz...</p>
          </div>
        )}

        {result && (
          <div className="results-grid">
            <div className="card">
              <h3>Transcript Preview</h3>
              <p>{result.transcript_preview}</p>
            </div>

            <div className="card">
              <h3>Summary Preview</h3>
              <p>{result.summary_preview}</p>
            </div>

            <div className="card">
              <h3>Translated Summary ({result.selected_language})</h3>
              <p>{result.translated_summary_preview}</p>
            </div>

            <div className="card">
              <h3>Quiz Questions</h3>
              <p>{result.quiz_preview}</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;