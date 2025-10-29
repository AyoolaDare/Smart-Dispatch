from pydantic import BaseModel

class Dispatch(BaseModel):
    id: str
    atm_id: str
    engineer_id: str
    status: str
