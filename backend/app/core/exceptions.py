from collections.abc import Mapping
from enum import StrEnum

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorCode(StrEnum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_TRANSITION = "INVALID_TRANSITION"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorBody(BaseModel):
    code: ErrorCode
    message: str
    details: list[ErrorDetail]


class ErrorResponse(BaseModel):
    """Error envelope shared by every endpoint: { "error": { code, message, details } }."""

    error: ErrorBody


class AppError(Exception):
    """Base class for errors services raise on purpose. Subclasses set the code and status."""

    code: ErrorCode = ErrorCode.INTERNAL_ERROR
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, details: list[ErrorDetail] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or []


HTTP_STATUS_TO_ERROR_CODE = {
    status.HTTP_401_UNAUTHORIZED: ErrorCode.UNAUTHENTICATED,
    status.HTTP_403_FORBIDDEN: ErrorCode.FORBIDDEN,
    status.HTTP_404_NOT_FOUND: ErrorCode.NOT_FOUND,
    status.HTTP_405_METHOD_NOT_ALLOWED: ErrorCode.METHOD_NOT_ALLOWED,
}
INTERNAL_ERROR_MESSAGE = "An unexpected error occurred."
VALIDATION_ERROR_MESSAGE = "The request is not valid."


def build_error_response(
    status_code: int,
    code: ErrorCode,
    message: str,
    details: list[ErrorDetail] | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    body = ErrorResponse(error=ErrorBody(code=code, message=message, details=details or []))
    return JSONResponse(
        status_code=status_code, content=body.model_dump(mode="json"), headers=headers
    )


def code_for_http_status(status_code: int) -> ErrorCode:
    if status_code in HTTP_STATUS_TO_ERROR_CODE:
        return HTTP_STATUS_TO_ERROR_CODE[status_code]
    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        return ErrorCode.INTERNAL_ERROR
    return ErrorCode.VALIDATION_ERROR


def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return build_error_response(exc.status_code, exc.code, exc.message, exc.details)


def handle_http_exception(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return build_error_response(
        exc.status_code,
        code_for_http_status(exc.status_code),
        str(exc.detail),
        headers=exc.headers,
    )


# Only where the error came from and what is wrong: FastAPI's default also echoes the
# submitted input, which could contain secrets.
def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        ErrorDetail(field=".".join(str(part) for part in error["loc"]), message=error["msg"])
        for error in exc.errors()
    ]
    return build_error_response(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        ErrorCode.VALIDATION_ERROR,
        VALIDATION_ERROR_MESSAGE,
        details,
    )


# Starlette re-raises after this handler responds, so uvicorn still logs the traceback.
def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCode.INTERNAL_ERROR, INTERNAL_ERROR_MESSAGE
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, handle_app_error)
    app.add_exception_handler(StarletteHTTPException, handle_http_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(Exception, handle_unexpected_error)
