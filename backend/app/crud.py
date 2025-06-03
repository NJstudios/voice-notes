# backend/app/crud.py
from datetime import datetime
from sqlalchemy.orm import Session
from openai import OpenAI
from . import models
from .config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def create_note(db: Session, transcript: str, duration: float) -> models.Note:
    """Insert a new Note row into the DB."""
    note = models.Note(
        transcript=transcript,
        duration=duration,
        recorded_at=datetime.utcnow()
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_last_summary(db: Session):
    """Return the most recent Summary (or None)."""
    return db.query(models.Summary).order_by(models.Summary.summary_at.desc()).first()

def get_notes_after(db: Session, since: datetime):
    """Fetch all Note rows with recorded_at > since."""
    return (
        db.query(models.Note)
        .filter(models.Note.recorded_at > since)
        .order_by(models.Note.recorded_at)
        .all()
    )

def create_summary(db: Session, range_start: datetime, range_end: datetime, content: str) -> models.Summary:
    """Insert a new Summary row into the DB."""
    summary = models.Summary(
        range_start=range_start,
        range_end=range_end,
        content=content,
        summary_at=datetime.utcnow()
    )
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary

def generate_summary_for_notes(db: Session):
    """
    1. Find last_summary.range_end (or epoch if none).
    2. Fetch notes recorded after that.
    3. If none, return None.
    4. Otherwise, stitch them into a prompt and call GPT.
    5. Insert a new Summary row.
    6. Return the new Summary.
    """
    last = get_last_summary(db)
    since = last.range_end if last else datetime.fromtimestamp(0)
    notes = get_notes_after(db, since)
    
    if not notes:
        return None

    # Build a simple timestamped transcript block
    combined = ""
    for n in notes:
        ts = n.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
        combined += f"[{ts}] {n.transcript}\n"

    prompt = f"""
You are an expert note-taker. Given these timestamped notes, produce a concise bullet-point summary (5–7 bullets, in chronological order):
{combined}
"""

    try:
        # New OpenAI API v1.0+ syntax
        response = client.chat.completions.create(
            model=settings.SUMMARY_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=400,
        )
        
        content = response.choices[0].message.content.strip()
        return create_summary(db, notes[0].recorded_at, notes[-1].recorded_at, content)
        
    except Exception as e:
        error_str = str(e).lower()
        
        # Handle quota exceeded for summary generation too
        if "quota" in error_str or "429" in error_str or "insufficient_quota" in error_str:
            print("⚠️  OpenAI quota exceeded - using mock summary")
            content = f"[MOCK SUMMARY] Summary of {len(notes)} notes from {notes[0].recorded_at.strftime('%Y-%m-%d %H:%M')} to {notes[-1].recorded_at.strftime('%Y-%m-%d %H:%M')}. OpenAI quota exceeded - please add credits for real summaries."
            return create_summary(db, notes[0].recorded_at, notes[-1].recorded_at, content)
        else:
            print(f"Summary generation error: {str(e)}")
            raise Exception(f"Summary generation failed: {e}")