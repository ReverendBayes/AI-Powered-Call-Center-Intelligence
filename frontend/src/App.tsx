// --- Main UI App for Call Intelligence ---
// Handles audio upload and text transcript upload as separate modes
// Uses React state to toggle views and send data to FastAPI backend

import React, { useState } from 'react';
import './App.css';
import TextUpload from './TextUpload';

function App() {
  // track which mode user is in (audio or text)
  const [mode, setMode] = useState<'audio' | 'text'>('audio');

  // audio-specific state
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState('');
  const [insights, setInsights] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // handle audio file input
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setAudioFile(e.target.files[0]);
    }
  };

  // send audio to backend for Whisper + GPT analysis
  const handleUpload = async () => {
    if (!audioFile) {
      setError('Please select an audio file.');
      return;
    }

    setIsLoading(true);
    setError('');
    setTranscript('');
    setInsights('');

    const formData = new FormData();
    formData.append('file', audioFile);

    try {
      const response = await fetch('http://localhost:8000/analyze-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Server error during analysis.');
      }

      const data = await response.json();
      setTranscript(data.transcript);
      setInsights(data.insights);
    } catch (err: any) {
      setError(err.message || 'Unexpected error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">AI-Powered Call Center Intelligence</h1>

        <div className="mode-toggle">
          <label>
            <input
              type="radio"
              value="audio"
              checked={mode === 'audio'}
              onChange={() => setMode('audio')}
            />
            Upload Audio
          </label>
          <label>
            <input
              type="radio"
              value="text"
              checked={mode === 'text'}
              onChange={() => setMode('text')}
            />
            Upload Transcript
          </label>
        </div>

        {mode === 'audio' ? (
          <>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={isLoading}>
              {isLoading ? 'Analyzing...' : 'Upload and Analyze'}
            </button>

            {error && <p className="error-text">{error}</p>}

            {transcript && (
              <div className="output-block">
                <h2>Transcript</h2>
                <pre>{transcript}</pre>
              </div>
            )}

            {insights && (
              <div className="output-block">
                <h2>GPT Insights</h2>
                <pre>{insights}</pre>
              </div>
            )}
          </>
        ) : (
          <TextUpload />
        )}
      </div>
    </div>
  );
}

export default App;
