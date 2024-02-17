from src.authors.schemas import ResponseAuthorSchema
from sqlalchemy import select
from injector import Inject
from src.authors.interfaces import AuthorRepository
from src.authors.models import Author
from src.core.unit_of_work import UnitOfWork


class AuthorRepository(AuthorRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(self, author_id: int) -> ResponseAuthorSchema | None:
        query = select(Author).where(Author.key == author_id)
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        author = result.scalars().first()  # Fetch the first row
        if author:
            return ResponseAuthorSchema(
                key=author.key,
                name=author.name,
                birth_date=author.birth_date
            )
        return None

    async def create(self, author: Author) -> ResponseAuthorSchema:
        session = await self._unit_of_work.get_db_session()
        session.add(author)
        return await session.flush([author])
