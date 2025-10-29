from pydantic import BaseModel

class Alert(BaseModel):
    id: str
    atm_id: str
    message: str
    resolved: bool
