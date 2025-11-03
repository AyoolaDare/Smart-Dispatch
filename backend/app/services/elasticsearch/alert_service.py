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
