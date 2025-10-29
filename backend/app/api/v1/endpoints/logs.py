from fastapi import APIRouter
from app.models.schemas import ATMLog
from app.services.elasticsearch.es_client import es
from app.utils.logger import logger
import datetime

router = APIRouter()

@router.post("/logs")
async def create_log(log: ATMLog):
    """
    Receives ATM telemetry data and indexes it in Elasticsearch.
    """
    doc = log.dict()
    doc["timestamp"] = datetime.datetime.utcnow()
    res = await es.index(index="atm_logs", document=doc)
    logger.info(f"Indexed document with ID: {res['_id']}")
    return {"id": res["_id"], "message": "Log created successfully"}
