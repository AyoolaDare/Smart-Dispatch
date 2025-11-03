import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.alert.alert_detection import run_rule_checks

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

def start_scheduler():
    """
    Starts the scheduler and adds the periodic alert detection job.
    """
    try:
        scheduler.add_job(
            run_rule_checks,
            'interval',
            seconds=60, # As per requirements, re-check every 60 seconds
            id='alert_detection_job',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started and alert detection job added.")
    except Exception as e:
        logger.error(f"Error starting the scheduler: {e}")

def stop_scheduler():
    """
    Stops the scheduler.
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped.")
