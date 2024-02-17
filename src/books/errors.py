from src.core.exceptions import RequestException


class BookErrors:
    BOOK_NOT_FOUND = RequestException(
        "BOOK_NOT_FOUND",
        "The requested book was not found",
        404,
    )
    BOOK_ALREADY_EXISTS = RequestException(
        "BOOK_ALREADY_EXISTS",
        "The book is already registered against the barcode",
        400,
    )
    BOOK_CREATE_ERROR = RequestException(
        "BOOK_CREATE_ERROR",
        "An error occurred during book create",
        400,
    )
