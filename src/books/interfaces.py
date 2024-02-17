from typing import Protocol, runtime_checkable
from src.books.models import Book


@runtime_checkable
class BookRepository(Protocol):
    async def get_by_id(self, Book_id: str) -> Book | None:
        ...

    async def create(
        self,
        author: Book,
    ) -> None:
        ...
