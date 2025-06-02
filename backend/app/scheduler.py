# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .crud import generate_summary_for_notes
from .database import SessionLocal

def start_scheduler():
    scheduler = AsyncIOScheduler()
    # every hour at minute 0
    scheduler.add_job(job_wrapper, "cron", minute=0)
    scheduler.start()

def job_wrapper():
    db = SessionLocal()
    try:
        generate_summary_for_notes(db)
    finally:
        db.close()
