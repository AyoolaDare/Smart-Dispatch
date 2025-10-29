from app.services.elasticsearch.es_client import es
from app.utils.logger import logger

async def get_atm_status_aggregation():
    """
    Aggregates ATM status data from Elasticsearch.
    """
    logger.info("Fetching ATM status aggregation...")
    # This is a placeholder for a real aggregation query
    return {"up": 100, "down": 5, "maintenance": 2}
