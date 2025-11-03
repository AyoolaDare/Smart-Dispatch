import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.services.elasticsearch import log_query_service
from app.services.alert import alert_detection

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic model for the location data
class Location(BaseModel):
    lat: float
    lon: float

# Pydantic model for the incoming ATM telemetry log
class ATMLog(BaseModel):
    atm_id: str = Field(..., example="ATM-123")
    status: str = Field(..., example="error")
    uptime: float = Field(..., example=98.5)
    cash_level: int = Field(..., example=50)
    error_code: Optional[str] = Field(None, example="PRINTER_JAM")
    error_message: Optional[str] = Field(None, example="Paper jam detected")
    location: Location

@router.post("/logs/ingest", status_code=201)
async def ingest_log_endpoint(log: ATMLog):
    """
    Receives ATM telemetry data, indexes it into Elasticsearch,
    and performs a real-time check for alert conditions.
    """
    try:
        log_dict = log.dict()

        # Ingest the log into Elasticsearch
        doc_id = await log_query_service.ingest_log(log_dict)

        # Perform real-time alert check on the incoming log
        await alert_detection.check_single_log(log_dict)

        return {"message": "Log ingested successfully", "doc_id": doc_id}
    except Exception as e:
        logger.error(f"Error during log ingestion: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest log.")
