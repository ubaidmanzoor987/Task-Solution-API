from typing import Optional
from pydantic import BaseModel
from datetime import date

from src.authors.schemas import ResponseAuthorSchema


class ResponseBookSchema(BaseModel):
    key: int
    title: str
    barcode: str
    publish_year: int
    author: ResponseAuthorSchema
    quantity: Optional[int]

    class Config:
        orm_mode = True
