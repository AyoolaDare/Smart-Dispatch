import logging
import asyncio
from fastapi import FastAPI

from app.api.v1.endpoints import logs
from app.api.v1.endpoints import alerts_clean as alerts
from app.config import settings
from app.jobs.scheduler import start_scheduler, stop_scheduler
from app.services.elasticsearch.es_client import es_client
from app.services.elasticsearch.log_query_service import ensure_index_template_exists

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ATM Smart Dispatch - Log Ingestion and Alerting",
    description="This service ingests ATM telemetry and creates alerts for anomalies.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """
    Application startup logic:
    1. Ping Elasticsearch to ensure connection.
    2. Create the index template if it doesn't exist.
    3. Start the background job scheduler.
    """
    logger.info("Starting application...")
    # Bound the ping call so startup doesn't hang for a long time if ES is down.
    try:
        connected = await asyncio.wait_for(es_client.ping(), timeout=5)
    except asyncio.TimeoutError:
        logger.error("Timeout while trying to ping Elasticsearch.")
        connected = False

    if connected:
        try:
            await ensure_index_template_exists()
        except Exception as e:
            logger.error(f"Failed to ensure index template exists: {e}")
        start_scheduler()
    else:
        logger.critical("Failed to connect to Elasticsearch. Application will not start correctly.")
        # Application will continue running, but features requiring ES will fail.

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic:
    1. Stop the background job scheduler.
    2. Close the Elasticsearch connection.
    """
    logger.info("Shutting down application...")
    stop_scheduler()
    await es_client.close()

# Include the API routers
app.include_router(logs.router, prefix="/api/v1", tags=["Log Ingestion"])
app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"])
