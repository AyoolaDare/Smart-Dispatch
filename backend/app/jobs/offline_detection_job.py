from app.services.elasticsearch.es_client import es
from app.utils.logger import logger
from datetime import datetime, timedelta

async def detect_offline_atms():
    """
    Detects ATMs that have not sent telemetry data in the last 30 minutes.
    """
    logger.info("Running offline ATM detection job...")

    thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)

    query = {
        "query": {
            "range": {
                "timestamp": {
                    "lt": thirty_minutes_ago.isoformat()
                }
            }
        }
    }

    try:
        res = await es.search(index="atm_logs", body=query)
        offline_atms = [hit["_source"]["atm_id"] for hit in res["hits"]["hits"]]
        if offline_atms:
            logger.warning(f"Offline ATMs detected: {offline_atms}")
            # Here you would typically create an alert
        else:
            logger.info("No offline ATMs detected.")
    except Exception as e:
        logger.error(f"Error querying for offline ATMs: {e}")
