from typing import Any, Dict, Optional

from shared.utils.constants import ErrorCodes, ErrorMessages


class AppError(Exception):
    """Base class for all application exceptions."""

    def __init__(
        self,
        message: Optional[str],
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None,
        code: Optional[str] = ErrorCodes.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.code = code

    def to_dict(self) -> Dict[str, Any]:
        rv = dict(self.payload or ())
        rv["message"] = self.message
        rv["code"] = self.code if self.code else self.__class__.__name__
        return rv


class ResourceNotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: Optional[str] = ErrorMessages.RESOURCE_NOT_FOUND,
        payload: Optional[Dict[str, Any]] = None,
        code: Optional[str] = ErrorCodes.RESOURCE_NOT_FOUND,
    ):
        super().__init__(message, status_code=404, payload=payload, code=code)


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: Optional[str] = ErrorMessages.VALIDATION_FAILED,
        payload: Optional[Dict[str, Any]] = None,
        code: Optional[str] = ErrorCodes.VALIDATION_FAILED,
    ):
        super().__init__(message, status_code=400, payload=payload, code=code)


class DatabaseError(AppError):
    """Raised when a database operation fails."""

    def __init__(
        self,
        message: Optional[str] = ErrorMessages.DATABASE_ERROR,
        payload: Optional[Dict[str, Any]] = None,
        code: Optional[str] = ErrorCodes.DATABASE_ERROR,
    ):
        super().__init__(message, status_code=500, payload=payload, code=code)


class DatabaseConnectionError(DatabaseError):
    """Raised when the database connection is unavailable."""

    def __init__(
        self,
        message: Optional[str] = ErrorMessages.DATABASE_CONNECTION_ERROR,
        payload: Optional[Dict[str, Any]] = None,
        code: Optional[str] = ErrorCodes.DATABASE_CONNECTION_ERROR,
    ):
        super().__init__(message, payload=payload, code=code)


class InvalidRequestError(AppError):
    """Raised when the request itself is malformed or invalid (e.g., incorrect headers, missing required query params, improper method)."""

    def __init__(
        self,
        message: Optional[str] = ErrorMessages.INVALID_REQUEST,
        payload: Optional[Dict[str, Any]] = None,
        code: Optional[str] = ErrorCodes.INVALID_REQUEST,
    ):
        super().__init__(message, status_code=400, payload=payload, code=code)
