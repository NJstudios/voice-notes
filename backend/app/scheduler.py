# backend/app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .crud import generate_summary_for_notes
from .database import SessionLocal

def start_scheduler():
    """
    On startup, build an AsyncIOScheduler that runs generate_summary_for_notes() every hour.
    """
    scheduler = AsyncIOScheduler()
    # Run at minute 0 of every hour, in UTC by default.
    scheduler.add_job(wrapper, "cron", minute=0)
    scheduler.start()

def wrapper():
    # Each job needs its own DB session
    db = SessionLocal()
    try:
        generate_summary_for_notes(db)
    finally:
        db.close()
