// frontend/src/pages/Summaries.tsx
import React, { useEffect, useState } from 'react';
import { fetchSummaries, generateSummary } from '../services/api';

export default function Summaries() {
  const [summaries, setSummaries] = useState<any[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const loadSummaries = async () => {
    try {
      const data = await fetchSummaries();
      setSummaries(data);
    } catch {
      console.error('Could not load summaries');
    }
  };

  useEffect(() => {
    loadSummaries();
  }, []);

  const handleGenerate = async () => {
    setMessage('Generating...');
    try {
      const result = await generateSummary();
      if ((result as any).message) {
        setMessage((result as any).message);
      } else {
        setMessage(null);
        loadSummaries(); // refresh list
      }
    } catch {
      setMessage('Error generating summary.');
    }
  };

  return (
    <div>
      <h1>Summaries</h1>
      <button onClick={handleGenerate}>Generate Summary</button>
      {message && <p>{message}</p>}
      <ul>
        {summaries.map((s) => (
          <li key={s.id}>
            <strong>[{new Date(s.summary_at).toLocaleString()}]</strong>
            <pre>{s.content}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}
