from fastapi import APIRouter

router = APIRouter()

@router.post("/token")
async def login():
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}
