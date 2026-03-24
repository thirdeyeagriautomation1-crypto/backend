from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============= Error Codes =============

class ErrorCode(str, Enum):
    """Standard error codes for API responses"""
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    INVALID_INPUT = "INVALID_INPUT"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    DUPLICATE_RESOURCE = "DUPLICATE_RESOURCE"


# ============= Custom Exception =============

class APIException(Exception):
    """Custom API exception for standardized error responses"""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
        status_code: int = 500,
        detail: dict = None
    ):
        """
        Initialize API exception
        
        Args:
            message: Human-readable error message
            error_code: ErrorCode enum value
            status_code: HTTP status code
            detail: Optional additional error details
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


# ============= Exception Handlers =============

async def api_exception_handler(request: Request, exc: APIException):
    """Handler for custom APIException"""
    logger.warning(f"APIException: {exc.message} ({exc.error_code}) - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "error_code": exc.error_code,
            "detail": exc.detail if exc.detail else None
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTPException: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {str(exc)} - {request.url}")

    cleaned_errors = []
    for err in exc.errors():
        cleaned_err = err.copy()
        # The 'input' key often contains the raw request body, which can be bytes.
        if 'input' in cleaned_err and isinstance(cleaned_err['input'], bytes):
            cleaned_err['input'] = cleaned_err['input'].decode('utf8', errors='ignore')

        # Convert any non-serializable 'ctx' values to strings
        if "ctx" in cleaned_err and cleaned_err["ctx"] is not None and isinstance(cleaned_err["ctx"], dict):
            cleaned_err["ctx"] = {k: str(v) for k, v in cleaned_err["ctx"].items()}
        cleaned_errors.append(cleaned_err)

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "detail": cleaned_errors
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc} - {request.url}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
        }
    )
