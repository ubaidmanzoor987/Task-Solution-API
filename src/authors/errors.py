from src.core.exceptions import RequestException


class AuthorErrors:
    AUTHOR_NOT_FOUND = RequestException(
        "AUTHOR_NOT_FOUND",
        "The requested user was not found",
        404,
    )
    AUTHOR_ALREADY_EXISTS = RequestException(
        "AUTHOR_ALREADY_EXISTS",
        "This user is already registered with this or another Organization",
        400,
    )
    AUTHOR_CREATE_ERROR = RequestException(
        "AUTHOR_CREATE_ERROR",
        "An error occurred during user update",
        400,
    )
