# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.lifespan import lifespan
from app.api.router import api_router

# --- 1. Инициализация приложения ---
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    redirect_slashes=False,  # <--- ДОБАВЬТЕ ЭТУ СТРОКУ (отключает 307 редирект)
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# --- 2. Регистрация обработчиков исключений ---
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# --- 3. Подключение Middleware ---
# Порядок важен: Security -> Logging -> CORS
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Подключение API роутеров ---
app.include_router(api_router, prefix="/api")

# --- 5. Раздача статических файлов (Локальное хранилище) ---
# В продакшене это должен делать Nginx напрямую из папки storage/
storage_path = os.path.abspath(settings.LOCAL_STORAGE_PATH)
if os.path.exists(storage_path):
    app.mount("/storage", StaticFiles(directory=storage_path), name="storage")

# --- 6. Базовый Health Check ---
@app.get("/api/health", tags=["Health"], summary="Проверка работоспособности")
async def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0"
    }