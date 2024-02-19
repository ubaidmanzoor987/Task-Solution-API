from injector import Inject
from src.books.services.book_repository import BookRepository
from src.core.use_cases import UseCase, UseCaseHandler
from src.books.errors import BookErrors
from sqlalchemy.exc import IntegrityError
from src.storing_information.errors import Storing_Info_Errors
from src.storing_information.models import StoringInformation
import pandas as pd
from src.storing_information.services.storing_information import StoringInformationRepository
from src.storing_information.errors import Storing_Info_Errors
from fastapi import UploadFile, File
from typing import Annotated, List


class BulkLeftOver(UseCase):
    barcode: List[str]
    quantity: List[int]

    class Handler(UseCaseHandler["BulkLeftOver", None]):
        def __init__(
            self,
            book_repository: Inject[BookRepository],
            storing_information_repository: Inject[StoringInformationRepository],
        ) -> None:
            self._book_repository = book_repository
            self._storing_information_repository = storing_information_repository
        async def execute(self, use_case: "BulkLeftOver") -> None:
            print("use_case",use_case)
            for barcode ,quantity in zip(use_case.barcode , use_case.quantity):
                print(barcode,quantity)
                book = await self._book_repository.validate_book_by_barcode(barcode)
                if not book:
                    continue
                storing_info = await self._storing_information_repository.get_by_book_id(book.key)
                if storing_info:
                    if quantity > 0:
                        storing_info.quantity += quantity
                    else:
                        if storing_info.quantity + quantity < 0:
                            raise Storing_Info_Errors.QUANTITY_LOW
                    try:
                        await self._storing_information_repository.save(storing_info)
                    except IntegrityError:
                        raise Storing_Info_Errors.STORING_INFO_CREATE_ERROR
                else:
                    try:
                        storing_info = StoringInformation(
                            book_id=book.key,
                            quantity=quantity,
                        )
                        await self._storing_information_repository.save(storing_info)
                    except IntegrityError:
                        raise Storing_Info_Errors.STORING_INFO_CREATE_ERROR
            # try:

            #     data = pd.read_excel(use_case.excel_file.file)

            #     for row_number, row in data.iterrows():
            #         try:
            #             barcode = str(row.iloc[0]).strip()
            #             quantity = pd.to_numeric(row.iloc[1], errors='coerce')
            #             print("quantity",quantity,barcode)

            #             if not barcode:
            #                 continue

            #             if pd.isna(quantity):
            #                 raise Storing_Info_Errors.BadRequestError(f"Invalid quantity at row {row_number}")

            #             book = await self._book_repository.validate_book_by_barcode(barcode)
            #             if not book:
            #                 raise Storing_Info_Errors.NotFoundError(f"Book not found at row {row_number}")

            #             storing_info = await self._storing_information_repository.get_by_book_id(book.key)

            #             if storing_info:
            #                 if quantity > 0:
            #                     storing_info.quantity += quantity
            #                 else:
            #                     if storing_info.quantity + quantity < 0:
            #                         raise Storing_Info_Errors.QUANTITY_LOW

            #                 await self._storing_information_repository.save(storing_info)
            #             else:
            #                 storing_info = StoringInformation(
            #                     book_id=book.key,
            #                     quantity=quantity,
            #                 )
            #                 await self._storing_information_repository.save(storing_info)
            #         except Exception as e:
            #             raise e

            # except Exception as e:
            #     raise e
