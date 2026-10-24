from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

class AppException(HTTPException):
    """Базовое исключение приложения."""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or "APP_ERROR"

class NotFoundException(AppException):
    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND")

class PermissionDeniedException(AppException):
    def __init__(self, detail: str = "Недостаточно прав"):
        super().__init__(status_code=403, detail=detail, error_code="PERMISSION_DENIED")

class ValidationException(AppException):
    def __init__(self, detail: str = "Ошибка валидации"):
        super().__init__(status_code=422, detail=detail, error_code="VALIDATION_ERROR")

class DuplicateException(AppException):
    def __init__(self, detail: str = "Запись уже существует"):
        super().__init__(status_code=409, detail=detail, error_code="DUPLICATE")

async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"AppException: {exc.error_code} - {exc.detail} | URL: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.error_code, "detail": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"]
        })
    logger.warning(f"Validation error on {request.url}: {errors}")
    return JSONResponse(
        status_code=422,
        content={"error_code": "VALIDATION_ERROR", "detail": errors}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error_code": "INTERNAL_ERROR", "detail": "Внутренняя ошибка сервера"}
    )