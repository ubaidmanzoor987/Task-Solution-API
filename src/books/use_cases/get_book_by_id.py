from injector import Inject
from src.books.errors import BookErrors
from src.books.schemas import ResponseBookSchema
from src.books.services.book_repository import BookRepository
from src.core.use_cases import UseCase, UseCaseHandler


class GetBookById(UseCase):
    book_id: int

    class Handler(UseCaseHandler["GetBookById", ResponseBookSchema]):
        def __init__(
            self,
            book_repository: Inject[BookRepository],
        ) -> None:
            self._book_repository = book_repository

        async def execute(self, use_case: "GetBookById") -> ResponseBookSchema:
            book = await self._book_repository.get_by_id(
                use_case.book_id
            )
            if not book:
                raise BookErrors.BOOK_NOT_FOUND

            return book
