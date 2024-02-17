from typing import Protocol, runtime_checkable
from src.authors.models import Author


@runtime_checkable
class AuthorRepository(Protocol):
    async def get_by_id(self, author_id: str) -> Author | None:
        ...

    async def create(
        self,
        author: Author,
    ) -> None:
        ...
