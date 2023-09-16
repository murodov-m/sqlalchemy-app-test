from pydantic import BaseModel
from typing import Optional


class ApplicationRequest(BaseModel):
    phone: str
    message: Optional[str] = None