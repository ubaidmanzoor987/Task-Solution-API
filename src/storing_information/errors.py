from src.core.exceptions import RequestException


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
