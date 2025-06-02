# app/schemas.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class NoteCreate(BaseModel):
    transcript: str
    duration: float
    recorded_at: datetime

class NoteOut(BaseModel):
    id: int
    recorded_at: datetime
    transcript: str
    duration: float
    processed_at: datetime

    class Config:
        orm_mode = True

class SummaryOut(BaseModel):
    id: int
    summary_at: datetime
    range_start: datetime
    range_end: datetime
    content: str

    class Config:
        orm_mode = True
