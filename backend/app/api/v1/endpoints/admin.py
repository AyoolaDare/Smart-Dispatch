from fastapi import APIRouter

router = APIRouter()

@router.get("/admin/status")
async def get_admin_status():
    return {"status": "ok"}
