// frontend/src/pages/Home.tsx
import React, { useEffect, useState } from 'react';
import VoiceRecorder from '../components/VoiceRecorder';
import { fetchNotes } from '../services/api';

export default function Home() {
  const [notes, setNotes] = useState<any[]>([]);

  // On mount, fetch all notes
  useEffect(() => {
    (async () => {
      try {
        const data = await fetchNotes();
        setNotes(data);
      } catch {
        console.error('Could not load notes');
      }
    })();
  }, []);

  return (
    <div>
      <h1>Voice Notes</h1>
      <VoiceRecorder />
      <h2>Recent Transcripts</h2>
      <ul>
        {notes.map((n) => (
          <li key={n.id}>
            [{new Date(n.recorded_at).toLocaleString()}]: {n.transcript}
          </li>
        ))}
      </ul>
    </div>
  );
}
