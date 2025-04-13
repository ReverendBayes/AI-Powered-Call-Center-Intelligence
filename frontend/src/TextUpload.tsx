// --- Transcript Upload UI with Clean Styling ---
// Supports manual paste or file-based transcript upload

import React, { useState } from 'react';
import './App.css';

function TextUpload() {
  const [transcript, setTranscript] = useState('');
  const [insights, setInsights] = useState('');
  const [inputText, setInputText] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // handle changes to pasted or typed text
  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
  };

  // handle uploaded .txt files
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      setInputText(text);
    };
    reader.readAsText(file);
  };

  // send transcript to FastAPI for GPT analysis
  const handleSubmit = async () => {
    if (!inputText.trim()) {
      setError('Transcript input is empty.');
      return;
    }

    setIsLoading(true);
    setError('');
    setTranscript('');
    setInsights('');

    const formData = new FormData();
    formData.append('transcript', inputText);

    try {
      const response = await fetch('http://localhost:8000/analyze-text', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze text.');
      }

      const data = await response.json();
      setTranscript(data.transcript);
      setInsights(data.insights);
    } catch (err: any) {
      setError(err.message || 'Unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 style={{ fontWeight: 600, marginBottom: '1rem' }}>
        Upload or Paste Transcript Text
      </h2>

      <textarea
        rows={10}
        placeholder="Paste transcript here..."
        value={inputText}
        onChange={handleTextChange}
      />

      <div>
        <input type="file" accept=".txt" onChange={handleFileUpload} />
      </div>

      <button onClick={handleSubmit} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Analyze Transcript'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {transcript && (
        <div>
          <h3>Transcript</h3>
          <pre>{transcript}</pre>
        </div>
      )}

      {insights && (
        <div>
          <h3>Insights</h3>
          <pre>{insights}</pre>
        </div>
      )}
    </div>
  );
}

export default TextUpload;