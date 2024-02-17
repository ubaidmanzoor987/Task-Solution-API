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

from src.storing_information.schemas import StoringInformationSchema


class BookRepository(BookRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(self, book_id: int) -> ResponseBookSchema | None:
        query = select(Book).where(Book.key == book_id).options(
            joinedload(Book.author),
            joinedload(Book.storing_information)  # Ensure storing_information is loaded eagerly
        )
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        book = result.scalars().first()  # Fetch the first row

        if book:
            # Validate author data
            author_data = None
            if book.author:
                author_data = ResponseAuthorSchema.model_validate(book.author)

            # Validate storing_information data
            storing_information_data = None
            if book.storing_information:
                storing_information_data = [
                    StoringInformationSchema(
                        book_id=info.book_id,
                        quantity=info.quantity,
                        date=info.date
                    )
                    for info in book.storing_information
                ]

            return ResponseBookSchema(
                key=book.key,
                barcode=book.barcode,
                author=author_data,
                publish_year=book.publish_year,
                title=book.title,
                quantity=storing_information_data[0].quantity if storing_information_data else 0
            )
        return None

    async def validate_book_by_barcode(
        self, barcode: str
    ) -> Book:
        query = select(Book).where(Book.barcode == barcode)
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        book = result.scalars().one_or_none()
        if not book:
            return None
        return book

    async def create(self, book: Book) -> ResponseBookSchema:
        session = await self._unit_of_work.get_db_session()
        session.add(book)
        await session.flush([book])

        # Fetch the associated author
        author = await session.get(Author, book.author_id)
        author_data = ResponseAuthorSchema.model_validate(author)

        return ResponseBookSchema(
            key=book.key,
            barcode=book.barcode,
            author=author_data,
            publish_year=book.publish_year,
            title=book.title,
            quantity=0
        )

    async def search_by_barcode(self, barcode: str) -> List[ResponseBookSchema]:
        query = select(Book).where(Book.barcode.like(f"{barcode}%")).options(
            joinedload(Book.author))
        # query = query.options(joinedload(Book.storing_information))
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        books = list(set(result.scalars().all()))

        response_books = []
        for book in books:
            author_data = None
            if book.author:
                author_data = ResponseAuthorSchema.model_validate(book.author)

            response_books.append(
                ResponseBookSchema(
                    key=book.key,
                    barcode=book.barcode,
                    author=author_data,
                    publish_year=book.publish_year,
                    title=book.title,
                    quantity=0
                )
            )
        return response_books
