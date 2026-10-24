# backend/app/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.core.logging import setup_logging
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    setup_logging()
    logger.info(f"🚀 Starting {settings.APP_NAME} API...")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")

    # TODO: Здесь можно инициализировать пул Redis, проверить подключение к MySQL
    # await redis_pool.ping()

    yield

    # --- SHUTDOWN ---
    logger.info("🛑 Shutting down API...")
    # TODO: Закрытие соединений с БД, Redis, отправка финальных метрик