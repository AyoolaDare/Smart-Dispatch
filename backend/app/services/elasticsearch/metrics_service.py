from app.services.elasticsearch.es_client import es
from app.utils.logger import logger

async def get_mttr_metrics():
    """
    Calculates the Mean Time to Repair (MTTR) for ATMs.
    """
    logger.info("Fetching MTTR metrics...")
    # This is a placeholder for a real aggregation query
    return {"mttr": "3.5 hours"}

async def get_uptime_metrics():
    """
    Calculates the uptime for ATMs.
    """
    logger.info("Fetching uptime metrics...")
    # This is a placeholder for a real aggregation query
    return {"uptime": "99.9%"}
