// frontend/src/services/api.ts
export async function uploadAudio(blob: Blob) {
  // Wraps POST /api/notes/record
  const form = new FormData();
  form.append('file', blob, 'note.webm');
  const res = await fetch('/api/notes/record', { method: 'POST', body: form });
  if (!res.ok) throw new Error('Upload failed');
  return res.json(); // { id, recorded_at, transcript, ... }
}

export async function fetchNotes() {
  const res = await fetch('/api/notes');
  if (!res.ok) throw new Error('Could not fetch notes');
  return res.json(); // NoteOut[]
}

export async function generateSummary() {
  const res = await fetch('/api/summaries/generate', { method: 'POST' });
  if (!res.ok) throw new Error('Summary generation failed');
  return res.json(); // SummaryOut or { message }
}

export async function fetchSummaries() {
  const res = await fetch('/api/summaries');
  if (!res.ok) throw new Error('Could not fetch summaries');
  return res.json(); // SummaryOut[]
}
