from pydantic import BaseModel

class Asset(BaseModel):
    id: str
    location: str
    status: str
