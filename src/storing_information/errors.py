from src.core.exceptions import RequestException
from fastapi import HTTPException
from starlette import status


class Storing_Info_Errors:
    STORING_INFO_NOT_FOUND = RequestException(
        "STORING_INFO_NOT_FOUND",
        "The requested Storing_Info was not found",
        404,
    )
    QUANTITY_LOW = RequestException(
        "QUANTITY_LOW",
        "The quantity is less than zero",
        400,
    )
    STORING_INFO_UPDATE_ERROR = RequestException(
        "STORING_INFO_UPDATE_ERROR",
        "An error occurred during Storing Info update",
        400,
    )


class BadRequestError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class NotFoundError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
