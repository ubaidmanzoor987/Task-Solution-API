from typing import Optional
from pydantic import BaseModel
from datetime import date


class StoringInformationSchema(BaseModel):
    book_id: int
    quantity: int
    date: Optional[date]
