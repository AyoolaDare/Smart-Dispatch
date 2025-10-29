from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.logger import logger

scheduler = AsyncIOScheduler()

def start_scheduler():
    """Start the APScheduler."""
    logger.info("Starting scheduler...")
    scheduler.start()
    logger.info("Scheduler started.")

def stop_scheduler():
    """Stop the APScheduler."""
    logger.info("Stopping scheduler...")
    scheduler.shutdown()
    logger.info("Scheduler stopped.")
