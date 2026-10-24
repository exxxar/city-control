from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.attachment import Attachment
from app.models.media_privacy_job import MediaPrivacyJob, PrivacyJobStatus
from app.integrations.storage.local_storage import storage
from loguru import logger


@shared_task(bind=True, max_retries=2)
def process_media_privacy(self, job_id: int):
    """Обрабатывает медиа-файл (размытие лиц/номеров)."""
    db: Session = SessionLocal()
    try:
        job = db.get(MediaPrivacyJob, job_id)
        if not job or job.status == PrivacyJobStatus.DONE:
            return

        job.status = PrivacyJobStatus.PROCESSING
        db.commit()

        attachment = db.get(Attachment, job.attachment_id)
        if not attachment:
            raise ValueError("Attachment not found")

        # --- МОК ОБРАБОТКИ ---
        # В реальности:
        # 1. Скачать оригинал из storage
        # 2. Передать в OpenCV / YOLO для поиска лиц и номеров
        # 3. Размыть найденные области
        # 4. Сохранить обработанное фото
        import time
        time.sleep(2)  # Имитация тяжелой работы

        # Копируем "обработанное" фото (в реальности это будет новое фото)
        processed_path = attachment.file_url.replace("originals", "processed")
        # storage.copy(attachment.file_url, processed_path)

        job.processed_file_url = processed_path
        job.status = PrivacyJobStatus.DONE
        db.commit()
        logger.info(f"Media privacy job {job_id} completed")

    except Exception as exc:
        logger.error(f"Error in media privacy job {job_id}: {exc}")
        job.status = PrivacyJobStatus.FAILED
        job.error_message = str(exc)
        db.commit()
        self.retry(exc=exc, countdown=30)
    finally:
        db.close()