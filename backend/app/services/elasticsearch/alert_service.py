import logging
from datetime import datetime
from app.services.elasticsearch.es_client import es
from app.utils.constants import ALERTS_INDEX_NAME

logger = logging.getLogger(__name__)

async def create_alert(alert_data: dict) -> str:
    """
    Indexes an alert document into the alerts index.

    Args:
        alert_data: A dictionary containing the alert information.

    Returns:
        The document ID of the indexed alert.
    """
    try:
        alert_data["timestamp"] = datetime.utcnow()
        res = await es.index(index=ALERTS_INDEX_NAME, document=alert_data)
        logger.info(f"Successfully created alert for ATM {alert_data.get('atm_id')} with doc ID {res['_id']}")
        return res["_id"]
    except Exception as e:
        logger.error(f"Error creating alert for ATM {alert_data.get('atm_id')}: {e}")
        raise

async def get_all_alerts(size: int = 100) -> list:
    """
    Retrieves all alerts from the alerts index.

    Args:
        size: The maximum number of alerts to return.

    Returns:
        A list of alert documents.
    """
    try:
        query = {"query": {"match_all": {}}}
        res = await es.search(index=ALERTS_INDEX_NAME, body=query, size=size)
        logger.info(f"Successfully retrieved {len(res['hits']['hits'])} alerts.")
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error retrieving alerts: {e}")
        # In a real app, you might want to differentiate between "index not found" and other errors.
        # For now, we return an empty list.
        return []
