from sqlalchemy.orm import Session
from app.models.attachment import Attachment
from app.models.media_privacy_job import MediaPrivacyJob, PrivacyJobStatus

class MediaPrivacyService:
    def __init__(self, db: Session):
        self.db = db

    def schedule_blurring(self, attachment_id: int, blur_faces: bool = True, blur_plates: bool = True):
        """Создает задачу на обработку медиа (в реальности триггерит Celery task)."""
        job = MediaPrivacyJob(
            attachment_id=attachment_id, status=PrivacyJobStatus.PENDING,
            blur_faces=blur_faces, blur_plates=blur_plates
        )
        self.db.add(job)
        self.db.commit()
        # TODO: media_tasks.process_privacy_job.delay(job.id)