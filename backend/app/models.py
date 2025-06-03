# backend/app/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    transcript = Column(Text, nullable=False)
    duration = Column(Numeric, nullable=False)
    processed_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    summary_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    range_start = Column(DateTime, nullable=False)
    range_end = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
