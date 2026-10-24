import sys
from loguru import logger
from app.core.config import settings


def setup_logging():
    logger.remove()  # Удаляем дефолтный handler

    log_level = "DEBUG" if settings.DEBUG else "INFO"

    # Консольный вывод
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # Файловый вывод (опционально)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    logger.info(f"Logging initialized. Level: {log_level}")