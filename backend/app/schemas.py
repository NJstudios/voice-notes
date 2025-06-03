# backend/app/schemas.py
from datetime import datetime
from pydantic import BaseModel

class NoteOut(BaseModel):
    id: int
    recorded_at: datetime
    transcript: str
    duration: float
    processed_at: datetime

    class Config:
        from_attributes = True   # v2 replaces orm_mode
        # tells Pydantic to read attributes from ORM objects

class SummaryOut(BaseModel):
    id: int
    summary_at: datetime
    range_start: datetime
    range_end: datetime
    content: str

    class Config:
        from_attributes = True
