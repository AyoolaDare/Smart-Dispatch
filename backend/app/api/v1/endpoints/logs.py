import logging
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List

from app.services.elasticsearch import log_query_service

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
    Receives ATM telemetry data and indexes it into Elasticsearch.
    """
    try:
        log_dict = log.dict()
        # Ingest the log into Elasticsearch
        doc_id = await log_query_service.ingest_log(log_dict)
        return {"message": "Log ingested successfully", "doc_id": doc_id}
    except Exception as e:
        logger.error(f"Error during log ingestion: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest log.")

@router.get("/logs")
async def get_logs_endpoint(
    limit: Optional[int] = Query(100, ge=1, le=1000),
    days: Optional[int] = Query(7, ge=1, le=30)
):
    """
    Retrieves recent ATM telemetry logs with pagination and time filtering.
    """
    try:
        logs = await log_query_service.get_all_logs(size=limit, days=days)
        return {
            "message": "Logs retrieved successfully",
            "count": len(logs),
            "logs": logs
        }
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve logs.")

@router.get("/logs/{atm_id}")
async def get_atm_logs_endpoint(
    atm_id: str,
    limit: Optional[int] = Query(100, ge=1, le=1000),
    days: Optional[int] = Query(7, ge=1, le=30)
):
    """
    Retrieves logs for a specific ATM with pagination and time filtering.
    """
    try:
        logs = await log_query_service.get_logs_by_atm(atm_id=atm_id, size=limit, days=days)
        return {
            "message": "Logs retrieved successfully",
            "atm_id": atm_id,
            "count": len(logs),
            "logs": logs
        }
    except Exception as e:
        logger.error(f"Error retrieving logs for ATM {atm_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs for ATM {atm_id}.")

@router.get("/logs/{atm_id}", response_model=List[dict])
async def get_atm_logs_endpoint(atm_id: str, limit: int = 100):
    """
    Retrieves logs for a specific ATM.
    """
    try:
        logs = await log_query_service.get_logs_by_atm(atm_id, size=limit)
        return logs
    except Exception as e:
        logger.error(f"Error retrieving logs for ATM {atm_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve logs.")
