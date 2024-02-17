from injector import Inject
from src.books.errors import BookErrors
from src.books.services.book_repository import BookRepository
from src.core.use_cases import UseCase, UseCaseHandler
from sqlalchemy.exc import IntegrityError
from src.storing_information.errors import Storing_Info_Errors
from src.storing_information.models import StoringInformation

from src.storing_information.services.storing_information import StoringInformationRepository


class RemoveLeftOver(UseCase):
    barcode: str
    quantity: int

    class Handler(UseCaseHandler["RemoveLeftOver", None]):
        def __init__(
            self,
            book_repository: Inject[BookRepository],
            storing_information_repository: Inject[StoringInformationRepository],
        ) -> None:
            self._book_repository = book_repository
            self._storing_information_repository = storing_information_repository

        async def execute(self, use_case: "RemoveLeftOver") -> None:
            book = await self._book_repository.validate_book_by_barcode(use_case.barcode)
            if not book:
                raise BookErrors.BOOK_NOT_FOUND
            storing_info = await self._storing_information_repository.get_by_book_id(book.key)
            if storing_info:
                if use_case.quantity > 0:
                    storing_info.quantity -= use_case.quantity
                else:
                    if storing_info.quantity - use_case.quantity < 0:
                        raise Storing_Info_Errors.QUANTITY_LOW
                try:
                    await self._storing_information_repository.save(storing_info)
                except IntegrityError:
                    raise Storing_Info_Errors.STORING_INFO_CREATE_ERROR
            else:
                try:
                    storing_info = StoringInformation(
                        book_id=book.key,
                        quantity=use_case.quantity,
                    )
                    await self._storing_information_repository.save(storing_info)
                except IntegrityError:
                    raise Storing_Info_Errors.STORING_INFO_CREATE_ERROR
