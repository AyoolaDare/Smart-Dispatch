from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_metrics():
    return {"message": "Dashboard metrics retrieved successfully"}
