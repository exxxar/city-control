import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Логируем начало запроса
        logger.info(f"→ {request.method} {request.url.path}")

        response = await call_next(request)

        # Логируем завершение с временем выполнения
        process_time = time.time() - start_time
        logger.info(
            f"← {request.method} {request.url.path} | Status: {response.status_code} | Time: {process_time:.3f}s")

        response.headers["X-Process-Time"] = str(process_time)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response