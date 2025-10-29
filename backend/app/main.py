from fastapi import FastAPI
from app.api.v1.endpoints import logs, dispatches, engineers, alerts, dashboard, auth, admin
from app.services.elasticsearch.es_client import es
from app.utils.logger import logger
from app.jobs.scheduler import scheduler, start_scheduler, stop_scheduler
from app.jobs.offline_detection_job import detect_offline_atms
import asyncio

app = FastAPI(title="ATM Smart Dispatch System")

@app.on_event("startup")
async def startup_event():
    logger.info("Connecting to Elasticsearch...")
    try:
        await es.info()
        logger.info("Successfully connected to Elasticsearch.")
    except Exception as e:
        logger.error(f"Could not connect to Elasticsearch: {e}")

    scheduler.add_job(detect_offline_atms, "interval", minutes=10)
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()

app.include_router(logs.router, prefix="/api/v1", tags=["logs"])
app.include_router(dispatches.router, prefix="/api/v1", tags=["dispatches"])
app.include_router(engineers.router, prefix="/api/v1", tags=["engineers"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["dashboard"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
