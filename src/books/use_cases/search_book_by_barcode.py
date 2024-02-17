from typing import List, Optional
from fastapi import Query
from injector import Inject
from src.books.schemas import ResponseBookSchema
from src.books.services.book_repository import BookRepository

from src.core.use_cases import UseCase, UseCaseHandler


class SearchBooksByBarcode(UseCase):
    barcode: Optional[str] = Query(None, title="Barcode to search")

    class Handler(UseCaseHandler["SearchBooksByBarcode", List[ResponseBookSchema]]):
        def __init__(
            self,
            book_repository: Inject[BookRepository],
        ) -> None:
            self._book_repository = book_repository

        async def execute(self, use_case: "SearchBooksByBarcode") -> List[ResponseBookSchema]:
            books = await self._book_repository.search_by_barcode(use_case.barcode)
            return books
