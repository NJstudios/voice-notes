// frontend/src/components/VoiceRecorder.tsx
import React, { useRef, useState } from 'react';
import { uploadAudio } from '../services/api';

export default function VoiceRecorder() {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);

  const startRecording = async () => {
    // 1. Ask for microphone permission
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    // 2. Create a MediaRecorder on that stream
    const mr = new MediaRecorder(stream, { mimeType: 'audio/webm; codecs=opus' });
    mediaRecorderRef.current = mr;
    const chunks: BlobPart[] = [];

    mr.ondataavailable = (e) => {
      // Collect recorded audio data
      chunks.push(e.data);
    };

    mr.onstop = async () => {
      // 3. Create a Blob from collected chunks
      const blob = new Blob(chunks, { type: 'audio/webm' });
      try {
        const json = await uploadAudio(blob);
        setTranscript(json.transcript);
      } catch (err) {
        console.error(err);
        setTranscript('Transcription failed');
      }
    };

    mr.start();
    setRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  return (
    <div>
      {recording ? (
        <button onClick={stopRecording}>Stop Recording</button>
      ) : (
        <button onClick={startRecording}>Start Recording</button>
      )}
      {transcript && (
        <div>
          <h3>Latest Transcript:</h3>
          <p>{transcript}</p>
        </div>
      )}
    </div>
  );
}
