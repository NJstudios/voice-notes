# backend/app/main.py
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from .database import engine, SessionLocal
from .models import Base, Note, Summary
from .schemas import NoteOut, SummaryOut
from .crud import create_note, get_last_summary, generate_summary_for_notes
from .audio_utils import transcribe_file
from .scheduler import start_scheduler
from .deps import get_db  # yields SessionLocal()

# 1. Create tables if they don't exist
Base.metadata.create_all(bind=engine)
app = FastAPI()
start_scheduler()  # start the hourly summary job

@app.post("/api/notes/record", response_model=NoteOut)
async def record_note(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    1. Receive an audio file (WebM, WAV, etc.) from the client.
    2. Save it to a temporary path.
    3. Call Whisper to transcribe.
    4. Insert into the notes table.
    5. Return the new Note as JSON.
    """
    # 1. Save upload to temporary directory (cross-platform)
    timestamp = datetime.utcnow().timestamp()
    
    # Create a temporary file with proper extension
    temp_dir = tempfile.gettempdir()
    filename = file.filename or "audio.webm"
    temp_path = os.path.join(temp_dir, f"{timestamp}_{filename}")
    
    try:
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"File saved to: {temp_path}")
        print(f"File size: {os.path.getsize(temp_path)} bytes")
        
        # 2. Transcribe (fixed variable name)
        print("Starting transcription...")
        result = transcribe_file(temp_path)
        print(f"Transcription result: {result}")
        
        transcript = result.get("text", "")
        duration = result.get("duration", 0.0)
        
        # 3. Persist
        note_obj = create_note(db, transcript, duration)
        
        return note_obj
        
    except Exception as e:
        print(f"Full error details: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass  # If cleanup fails, continue anyway

@app.get("/api/notes", response_model=list[NoteOut])
def read_notes(db: Session = Depends(get_db)):
    """Return all notes, newest first."""
    notes = db.query(Note).order_by(Note.recorded_at.desc()).all()
    return notes

@app.post("/api/summaries/generate", response_model=SummaryOut | dict)
def generate_summary(db: Session = Depends(get_db)):
    """
    Manually invoke summary generation (same logic as scheduler).
    If no new notes, return {"message": "..."}.
    Otherwise return the newly created Summary.
    """
    last = get_last_summary(db)
    new_summary = generate_summary_for_notes(db)
    if not new_summary:
        return {"message": "No new notes to summarize."}
    return new_summary

@app.get("/api/summaries", response_model=list[SummaryOut])
def read_summaries(db: Session = Depends(get_db)):
    """Return all summaries, newest first."""
    return db.query(Summary).order_by(Summary.summary_at.desc()).all()