import logging
from datetime import datetime, timedelta
from app.services.elasticsearch.es_client import es_client
from app.utils.constants import (
    TELEMETRY_INDEX_PREFIX,
    TELEMETRY_INDEX_TEMPLATE,
    TELEMETRY_INDEX_TEMPLATE_NAME,
)

logger = logging.getLogger(__name__)

async def ingest_log(log_data: dict) -> str:
    """
    Ingests a single ATM telemetry log into a daily index.

    Args:
        log_data: A dictionary containing the ATM telemetry data.

    Returns:
        The document ID of the indexed log.
    """
    try:
        # Add a timestamp and determine the daily index name
        log_data["timestamp"] = datetime.utcnow()
        index_name = f"{TELEMETRY_INDEX_PREFIX}-{datetime.utcnow().strftime('%Y.%m.%d')}"

        # Index the document
        client = await es_client.get_client()
        res = await client.index(index=index_name, document=log_data)
        logger.info(f"Successfully indexed log for ATM {log_data.get('atm_id')} with doc ID {res['_id']}")
        return res["_id"]
    except Exception as e:
        logger.error(f"Error indexing log for ATM {log_data.get('atm_id')}: {e}")
        raise

async def get_all_logs(size: int = 100, days: int = 7) -> list:
    """
    Retrieves recent ATM telemetry logs.

    Args:
        size: Maximum number of logs to return
        days: Number of days of history to search

    Returns:
        List of log documents
    """
    try:
        client = await es_client.get_client()
        start_time = datetime.utcnow() - timedelta(days=days)
        
        query = {
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {
                "range": {
                    "timestamp": {
                        "gte": start_time.isoformat()
                    }
                }
            }
        }
        
        index_pattern = f"{TELEMETRY_INDEX_PREFIX}-*"
        res = await client.search(index=index_pattern, body=query, size=size)
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        return []

async def get_logs_by_atm(atm_id: str, size: int = 100, days: int = 7) -> list:
    """
    Retrieves logs for a specific ATM.

    Args:
        atm_id: The ATM ID to fetch logs for
        size: Maximum number of logs to return
        days: Number of days of history to search

    Returns:
        List of log documents for the specified ATM
    """
    try:
        client = await es_client.get_client()
        start_time = datetime.utcnow() - timedelta(days=days)
        
        query = {
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {
                "bool": {
                    "must": [
                        {"term": {"atm_id.keyword": atm_id}},
                        {"range": {"timestamp": {"gte": start_time.isoformat()}}}
                    ]
                }
            }
        }
        
        index_pattern = f"{TELEMETRY_INDEX_PREFIX}-*"
        res = await client.search(index=index_pattern, body=query, size=size)
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error retrieving logs for ATM {atm_id}: {e}")
        return []

async def ensure_index_template_exists():
    """
    Checks if the ATM telemetry index template exists and creates it if not.
    This ensures that new daily indices are created with the correct mapping.
    """
    try:
        client = await es_client.get_client()
        template_exists = await client.indices.exists_index_template(name=TELEMETRY_INDEX_TEMPLATE_NAME)
        if not template_exists:
            logger.info(f"Index template '{TELEMETRY_INDEX_TEMPLATE_NAME}' not found. Creating it.")
            await client.indices.put_index_template(
                name=TELEMETRY_INDEX_TEMPLATE_NAME,
                body=TELEMETRY_INDEX_TEMPLATE
            )
            logger.info(f"Successfully created index template '{TELEMETRY_INDEX_TEMPLATE_NAME}'.")
        else:
            logger.info(f"Index template '{TELEMETRY_INDEX_TEMPLATE_NAME}' already exists.")
    except Exception as e:
        logger.error(f"Error ensuring index template exists: {e}")
        raise
