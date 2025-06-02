# app/crud.py
from datetime import datetime
from sqlalchemy.orm import Session
import openai

from . import models, schemas
from .config import settings

openai.api_key = settings.OPENAI_API_KEY

def create_note(db: Session, transcript: str, duration: float) -> models.Note:
    note = models.Note(transcript=transcript, duration=duration, recorded_at=datetime.utcnow())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes_after(db: Session, ts):
    return db.query(models.Note).filter(models.Note.recorded_at > ts).order_by(models.Note.recorded_at).all()

def create_summary(db: Session, range_start, range_end, content: str) -> models.Summary:
    summary = models.Summary(
        summary_at=datetime.utcnow(),
        range_start=range_start,
        range_end=range_end,
        content=content
    )
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary

def get_last_summary(db: Session):
    return db.query(models.Summary).order_by(models.Summary.summary_at.desc()).first()

def generate_summary_for_notes(db: Session):
    last = get_last_summary(db)
    since = last.range_end if last else datetime.fromtimestamp(0)
    notes = get_notes_after(db, since)
    if not notes:
        return None

    combined = ""
    for n in notes:
        combined += f"[{n.recorded_at.strftime('%Y-%m-%d %H:%M:%S')}] {n.transcript}\n"

    prompt = f"""
You are an expert note-taker. Given these timestamped notes, produce a concise bullet-point summary (5–7 bullets max), in chronological order:

{combined}
"""
    resp = openai.ChatCompletion.create(
        model=settings.SUMMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=400,
    )
    content = resp.choices[0].message.content.strip()
    start_ts = notes[0].recorded_at
    end_ts = notes[-1].recorded_at
    return create_summary(db, start_ts, end_ts, content)
