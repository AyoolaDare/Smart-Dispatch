from app.services.elasticsearch.es_client import es
from app.utils.logger import logger

async def get_logs_for_atm(atm_id: str):
    """
    Retrieves logs for a specific ATM from Elasticsearch.
    """
    logger.info(f"Fetching logs for ATM ID: {atm_id}")
    query = {"query": {"match": {"atm_id": atm_id}}}
    try:
        res = await es.search(index="atm_logs", body=query)
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error fetching logs for ATM {atm_id}: {e}")
        return []
