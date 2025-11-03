import logging
from fastapi import APIRouter
from typing import List

from app.services.elasticsearch import alert_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/alerts", response_model=List[dict])
async def get_alerts_endpoint():
    """
    Retrieves all alerts from the Elasticsearch `alerts` index.
    """
    try:
        alerts = await alert_service.get_all_alerts()
        return alerts
    except Exception as e:
        logger.error(f"Error in /alerts endpoint: {e}")
        # In a real app, you might return a proper HTTP error.
        # For now, we return an empty list.
        return []
