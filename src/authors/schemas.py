from typing import Optional
from pydantic import BaseModel
from datetime import date


class ResponseAuthorSchema(BaseModel):
    key: int
    name: str
    birth_date: Optional[date]

    class Config:
        from_attributes = True
