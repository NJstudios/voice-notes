# app/main.py
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from .database import engine
from .models import Base, Note, Summary
from .schemas import NoteOut, SummaryOut
from .deps import get_db
from .crud import create_note, generate_summary_for_notes, get_last_summary
from .audio_utils import transcribe_file
from .scheduler import start_scheduler

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
start_scheduler()

@app.post("/api/notes/record", response_model=NoteOut)
async def record_note(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save upload to /tmp
    timestamp = datetime.utcnow().timestamp()
    temp_path = f"/tmp/{timestamp}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # 2. Transcribe via Whisper
    try:
        result = transcribe_file(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    transcript_text = result.get("text", "")
    duration = result.get("duration", 0.0)
    note = create_note(db, transcript_text, duration)
    return note

@app.get("/api/notes", response_model=list[NoteOut])
def read_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).order_by(Note.recorded_at.desc()).all()
    return notes

@app.post("/api/summaries/generate", response_model=SummaryOut | dict)
def generate_summary(db: Session = Depends(get_db)):
    last = get_last_summary(db)
    new_summary = generate_summary_for_notes(db)
    if not new_summary:
        return {"message": "No new notes to summarize."}
    return new_summary

@app.get("/api/summaries", response_model=list[SummaryOut])
def read_summaries(db: Session = Depends(get_db)):
    return db.query(Summary).order_by(Summary.summary_at.desc()).all()
