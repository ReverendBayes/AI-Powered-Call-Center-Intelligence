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

  // Format insights: label on top line, bolded answer below
  const formatInsights = (text: string) => {
    const lines = text
      .replace(/[\u{1F300}-\u{1F6FF}]/gu, '') // strip emojis
      .split('\n')
      .map((line) => {
        const match = line.match(/^(\d+\..*?):\s*(.*)$/);
        if (match) {
          return `<div style="margin-bottom: 1rem;">${match[1]}:<br/><strong>${match[2]}</strong></div>`;
        }
        return `<div style="margin-bottom: 1rem;">${line}</div>`;
      });
    return lines.join('');
  };

  // Format transcript: bold speaker names
  const formatTranscript = (text: string) => {
    return text
      .split('\n')
      .map((line) => {
	const match = line.match(/^\s*(Agent|Customer):\s*(.*)$/i);
        if (match) {
          return `<div style="margin-bottom: 0.75rem;"><strong>${match[1]}:</strong> ${match[2]}</div>`;
        }
        return `<div style="margin-bottom: 0.75rem;">${line}</div>`;
      })
      .join('');
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
  };

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
      const response = await fetch('http://localhost:8001/analyze-text', {
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

      {insights && (
        <div>
          <h3>Insights</h3>
          <div
            style={{
              whiteSpace: 'pre-wrap',
              fontFamily: 'Inter, sans-serif',
              lineHeight: '1.6',
              fontSize: '1rem',
              padding: '1rem',
              backgroundColor: '#f9f9f9',
              borderRadius: '8px',
            }}
            dangerouslySetInnerHTML={{ __html: formatInsights(insights) }}
          />
        </div>
      )}

      {transcript && (
        <div>
          <h3>Transcript</h3>
          <div
            style={{
              whiteSpace: 'pre-wrap',
              fontFamily: 'Inter, sans-serif',
              lineHeight: '1.6',
              fontSize: '1rem',
              padding: '1rem',
              backgroundColor: '#f9f9f9',
              borderRadius: '8px',
            }}
            dangerouslySetInnerHTML={{ __html: formatTranscript(transcript) }}
          />
        </div>
      )}
    </div>
  );
}

export default TextUpload;
