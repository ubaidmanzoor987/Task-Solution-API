from injector import Inject
from src.authors.errors import AuthorErrors
from src.authors.services.author_repository import AuthorRepository
from src.books.errors import BookErrors
from src.books.models import Book
from src.books.schemas import ResponseBookSchema
from src.books.services.book_repository import BookRepository
from src.core.use_cases import UseCase, UseCaseHandler
from sqlalchemy.exc import IntegrityError


class CreateBook(UseCase):
    barcode: str
    title: str
    publish_year: int
    author_id: int

    class Handler(UseCaseHandler["CreateBook", ResponseBookSchema]):
        def __init__(
            self,
            book_repository: Inject[BookRepository],
            author_repository: Inject[AuthorRepository],
        ) -> None:
            self._book_repository = book_repository
            self._author_repository = author_repository

        async def execute(self, use_case: "CreateBook") -> ResponseBookSchema:
            author = await self._author_repository.get_by_id(use_case.author_id)
            if not author:
                raise AuthorErrors.AUTHOR_NOT_FOUND
            get_book_by_barcode = await self._book_repository.validate_book_by_barcode(
                use_case.barcode
            )
            if get_book_by_barcode:
                raise BookErrors.BOOK_ALREADY_EXISTS
            book = Book(
                barcode=use_case.barcode,
                title=use_case.title,
                publish_year=use_case.publish_year,
                author_id=use_case.author_id,
            )
            try:
                book_created = await self._book_repository.create(book)
            except IntegrityError:
                raise BookErrors.BOOK_ALREADY_EXISTS

            return book_created
