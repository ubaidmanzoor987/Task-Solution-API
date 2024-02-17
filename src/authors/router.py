from collections.abc import Sequence
from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from src.authors.schemas import ResponseAuthorSchema
from src.core.use_cases import UseCase
from src.authors.use_cases import (
    CreateAuthor, GetAuthorById
)


router = APIRouter(
    prefix="/author",
    tags=["author"],
)


@router.get("/{auther_id}", description="Get a auther by id")
async def get_auther_by_id(
    use_case: Annotated[GetAuthorById, Depends()],
    handler: Annotated[GetAuthorById.Handler, Injected(GetAuthorById.Handler)],
) -> ResponseAuthorSchema:
    return await handler.execute(use_case)


class AnnotatedCreateAuthor(UseCase):
    name: Annotated[str, Body()]
    birth_date: Annotated[Optional[date], Body()]


@router.post("", description="Create a auther")
async def create_auther(
    use_case: Annotated[AnnotatedCreateAuthor, Body()],
    handler: Annotated[CreateAuthor.Handler, Injected(CreateAuthor.Handler)],
) -> ResponseAuthorSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(CreateAuthor(**use_case_dict))
