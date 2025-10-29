from fastapi import APIRouter

router = APIRouter()

@router.post("/dispatches")
async def create_dispatch():
    return {"message": "Dispatch created successfully"}
