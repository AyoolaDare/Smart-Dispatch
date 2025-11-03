import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.elasticsearch import alert_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/alerts", response_model=List[dict])
async def get_alerts_endpoint(limit: int = Query(100, ge=1, le=1000)):
    """
    Retrieves recent alerts from the Elasticsearch `alerts` index.
    """
    try:
        alerts = await alert_service.get_all_alerts(size=limit)
        return alerts
    except Exception as e:
        logger.error("Error in /alerts endpoint: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve alerts.")


@router.get("/alerts/stats")
async def get_alert_stats(
    days: Optional[int] = Query(7, ge=1, le=30, description="Number of days to analyze")
):
    """
    Get statistics about ATM incidents and alerts over a specified time period.
    Returns counts of incidents (errors, low cash, low uptime) and a breakdown of error types.
    """
    try:
        stats = await alert_service.get_incident_counts(days=days)
        return {
            "message": "Alert statistics retrieved successfully",
            "timeframe": f"Last {days} days",
            "stats": stats,
        }
    except Exception as e:
        logger.error("Failed to retrieve alert statistics: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve alert statistics.")
