from fastapi import APIRouter

router = APIRouter()

@router.get("/engineers")
async def get_engineers():
    return {"message": "Engineers retrieved successfully"}
