URL_REGEX = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"


class ErrorCodes:
    """
    Constants for error codes.
    """

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_CONNECTION_ERROR = "DATABASE_CONNECTION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"


class ErrorMessages:
    """
    Constants for error messages.
    """

    INVALID_PAGINATION = "Limit and offset parameters must be valid integers."
    LIMIT_EXCEEDED = (
        "Requested limit ({limit}) exceeds the maximum allowed limit of {max_limit}."
    )
    RESOURCE_NOT_FOUND = "Resource not found"
    VALIDATION_FAILED = "Validation failed"
    DATABASE_ERROR = "Database error occurred"
    DATABASE_CONNECTION_ERROR = "Database connection failed unexpectedly."
    INTERNAL_SERVER_ERROR = "An unexpected error occurred."
    INVALID_REQUEST = "The request was malformed or missing required parameters."
    NO_SELECTED_FILE = "No selected file"
    INVALID_IMAGE_TYPE = "File must be an image"
    IMAGE_SIZE_LIMIT_EXCEEDED = "Image must be less than 10MB"


class ThumbnailSizes:
    """
    Constants for thumbnail sizes.
    """

    SMALL = "300x300"
    MEDIUM = "600x600"
    LARGE = "1200x1200"
