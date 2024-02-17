from datetime import date
from typing import Optional
from injector import Inject
from src.authors.errors import AuthorErrors
from src.authors.models import Author
from src.authors.schemas import ResponseAuthorSchema
from src.authors.services.author_repository import AuthorRepository
from src.core.use_cases import UseCase, UseCaseHandler
from sqlalchemy.exc import IntegrityError


class CreateAuthor(UseCase):
    name: str
    birth_date: Optional[date]

    class Handler(UseCaseHandler["CreateAuthor", ResponseAuthorSchema]):
        def __init__(
            self,
            author_repository: Inject[AuthorRepository],
        ) -> None:
            self._access_point_repository = author_repository

        async def execute(self, use_case: "CreateAuthor") -> ResponseAuthorSchema:
            author = Author(name=use_case.name, birth_date=use_case.birth_date)
            try:
                await self._access_point_repository.create(author)
            except IntegrityError:
                raise AuthorErrors.AUTHOR_ALREADY_EXISTS

            return ResponseAuthorSchema.model_validate(author)
