from fastapi import APIRouter

router = APIRouter()

@router.get("/alerts")
async def get_alerts():
    return {"message": "Alerts retrieved successfully"}
