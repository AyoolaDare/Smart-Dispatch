from pydantic import BaseModel

class Engineer(BaseModel):
    id: str
    name: str
    available: bool
