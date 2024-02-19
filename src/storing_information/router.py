from typing import Annotated
from fastapi import APIRouter, Body, UploadFile
from fastapi_injector import Injected
from src.core.use_cases import UseCase
from src.storing_information.use_cases import (
    AddLeftOver, RemoveLeftOver, BulkLeftOver
)
from fastapi import Depends
from fastapi import FastAPI, File, UploadFile
from fastapi import UploadFile, File, Form
from fastapi import UploadFile, File, HTTPException
import pandas as pd

router = APIRouter(
    prefix="/left-over",
    tags=["left-over"],
)


class AnnotatedLeftoverRequest(UseCase):
    barcode: Annotated[str, Body()]
    quantity: Annotated[int, Body()]


@router.post("/add", description="Add book leftover")
async def add_leftover(
    use_case: Annotated[AnnotatedLeftoverRequest, Body()],
    handler: Annotated[AddLeftOver.Handler, Injected(AddLeftOver.Handler)],
) -> dict:
    use_case_dict = dict(use_case)
    await handler.execute(AddLeftOver(**use_case_dict))
    return {"message": "Leftover updated successfully"}



@router.post("/remove", description="Remove book leftover")
async def add_leftover(
    use_case: Annotated[AnnotatedLeftoverRequest, Body()],
    handler: Annotated[RemoveLeftOver.Handler, Injected(RemoveLeftOver.Handler)],
) -> dict:
    use_case_dict = dict(use_case)
    await handler.execute(RemoveLeftOver(**use_case_dict))

    return {"message": "Leftover updated successfully"}


@router.post("/bulk-add", description="Bulk add book leftovers from Excel file")
async def bulk_add_leftovers(
    handler: Annotated[BulkLeftOver.Handler, Injected(BulkLeftOver.Handler)],
    excel_file: UploadFile = File(...)
) -> dict:
        excel_data = pd.read_excel(excel_file.file, header = None)
        barcode = excel_data.iloc[:, 0].tolist()
        quantity = excel_data.iloc[:, 1].tolist()
        barcode = [str(element) for element in barcode]
        data = {
             "barcode" : barcode,
             "quantity": quantity
        }
        use_case_dict = dict(data)
        
        await handler.execute(BulkLeftOver(**use_case_dict))     
        return {"message": "Bulk update successful"}