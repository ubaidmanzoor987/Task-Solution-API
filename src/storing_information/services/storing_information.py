from typing import List
from sqlalchemy import select
from injector import Inject
from src.authors.schemas import ResponseAuthorSchema
from src.books.errors import BookErrors
from src.books.interfaces import BookRepository
from src.authors.models import Author
from src.books.models import Book
from src.books.schemas import ResponseBookSchema
from src.core.unit_of_work import UnitOfWork
from sqlalchemy.orm import joinedload
from src.storing_information.interfaces import StoringInformationRepository

from src.storing_information.models import StoringInformation


class StoringInformationRepository(StoringInformationRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_book_id(self, book_id: int) -> ResponseBookSchema | None:
        query = select(StoringInformation).where(StoringInformation.book_id == book_id)
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        book = result.scalars().first()  # Fetch the first row
        return book

    async def save(self, storing_info: StoringInformation) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(storing_info)
        await session.flush([storing_info])
