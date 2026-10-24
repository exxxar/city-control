import os
import time
from celery import shared_task
from app.core.config import settings
from loguru import logger


@shared_task
def cleanup_temp_files():
    """Удаляет файлы из папки temp, которые старше 24 часов."""
    temp_dir = os.path.join(settings.LOCAL_STORAGE_PATH, "uploads", "temp")
    if not os.path.exists(temp_dir):
        return

    now = time.time()
    deleted_count = 0

    for filename in os.listdir(temp_dir):
        filepath = os.path.join(temp_dir, filename)
        if os.path.isfile(filepath):
            if now - os.path.getmtime(filepath) > 86400:  # 24 часа
                os.remove(filepath)
                deleted_count += 1

    logger.info(f"Cleanup task finished. Deleted {deleted_count} temp files.")