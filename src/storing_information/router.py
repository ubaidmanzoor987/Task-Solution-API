from typing import Annotated
from fastapi import APIRouter, Body
from fastapi_injector import Injected
from src.core.use_cases import UseCase
from src.storing_information.use_cases import (
    AddLeftOver, RemoveLeftOver
)


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


class AnnotatedLeftoverRequest(UseCase):
    barcode: Annotated[str, Body()]
    quantity: Annotated[int, Body()]


@router.post("/remove", description="Remove book leftover")
async def add_leftover(
    use_case: Annotated[AnnotatedLeftoverRequest, Body()],
    handler: Annotated[RemoveLeftOver.Handler, Injected(RemoveLeftOver.Handler)],
) -> dict:
    use_case_dict = dict(use_case)
    await handler.execute(RemoveLeftOver(**use_case_dict))
    return {"message": "Leftover updated successfully"}

# @router.get("/", description="Search books by barcode")
# async def search_books_by_barcode(
#     use_case: Annotated[SearchBooksByBarcode, Depends()],
#     handler: Annotated[SearchBooksByBarcode.Handler, Injected(SearchBooksByBarcode.Handler)],
# ) -> Dict[str, Union[int, List[ResponseBookSchema]]]:
#     books = await handler.execute(use_case)
#     return {"found": len(books), "items": books}
