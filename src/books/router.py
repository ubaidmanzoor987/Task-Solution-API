from collections.abc import Sequence
from datetime import date
from typing import Annotated, Dict, List, Optional, Union

from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from src.authors.schemas import ResponseAuthorSchema
from src.books.schemas import ResponseBookSchema
from src.core.use_cases import UseCase
from src.books.use_cases import (
    GetBookById, CreateBook, SearchBooksByBarcode
)


router = APIRouter(
    prefix="/book",
    tags=["book"],
)


@router.get("/{book_id}", description="Get a book by id")
async def get_book_by_id(
    use_case: Annotated[GetBookById, Depends()],
    handler: Annotated[GetBookById.Handler, Injected(GetBookById.Handler)],
) -> ResponseBookSchema:
    return await handler.execute(use_case)


class AnnotatedCreateBook(UseCase):
    barcode: Annotated[str, Body()]
    title: Annotated[str, Body()]
    publish_year: Annotated[int, Body()]
    author_id: Annotated[int, Body()]


@router.post("", description="Create a book")
async def create_book(
    use_case: Annotated[AnnotatedCreateBook, Body()],
    handler: Annotated[CreateBook.Handler, Injected(CreateBook.Handler)],
) -> ResponseBookSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(CreateBook(**use_case_dict))


@router.get("/", description="Search books by barcode")
async def search_books_by_barcode(
    use_case: Annotated[SearchBooksByBarcode, Depends()],
    handler: Annotated[SearchBooksByBarcode.Handler, Injected(SearchBooksByBarcode.Handler)],
) -> Dict[str, Union[int, List[ResponseBookSchema]]]:
    books = await handler.execute(use_case)
    return {"found": len(books), "items": books}
