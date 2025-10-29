from app.utils.logger import logger

async def create_alert(atm_id: str, message: str):
    """
    Creates an alert in Elasticsearch.
    """
    logger.info(f"Creating alert for ATM {atm_id}: {message}")
    # This is a mock implementation
    return {"alert_id": "ALERT789", "status": "created"}
