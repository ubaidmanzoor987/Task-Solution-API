from src.authors.services.author_repository import AuthorRepository
from src.authors.errors import AuthorErrors
from injector import Inject
from src.core.use_cases import UseCase, UseCaseHandler
from src.authors.schemas import ResponseAuthorSchema


class GetAuthorById(UseCase):
    author_id: int

    class Handler(UseCaseHandler["GetAuthorById", ResponseAuthorSchema]):
        def __init__(
            self,
            author_repository: Inject[AuthorRepository],
        ) -> None:
            self._author_repository = author_repository

        async def execute(self, use_case: "GetAuthorById") -> ResponseAuthorSchema:
            author = await self._author_repository.get_by_id(
                use_case.author_id
            )
            if not author:
                raise AuthorErrors.AUTHOR_NOT_FOUND

            return author
