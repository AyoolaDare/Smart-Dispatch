from pydantic import BaseModel
from typing import Optional

class ATMLog(BaseModel):
    atm_id: str
    status: str
    uptime: float
    cash_level: int
    error_code: Optional[str] = None
