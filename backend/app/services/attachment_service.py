import os
import uuid
from sqlalchemy.orm import Session
from app.models.attachment import Attachment
from app.core.config import settings


class AttachmentService:
    def __init__(self, db: Session):
        self.db = db

    def save_file(self, file_content: bytes, original_name: str, mime_type: str, entity_type: str, entity_id: int,
                  user_id: int) -> Attachment:
        # Генерируем безопасное имя
        ext = os.path.splitext(original_name)[1]
        safe_name = f"{uuid.uuid4()}{ext}"

        # Формируем путь (в реальности здесь вызов storage_integration)
        relative_path = f"uploads/originals/{safe_name}"
        full_path = os.path.join(settings.LOCAL_STORAGE_PATH, relative_path)

        # Создаем директорию и пишем файл
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(file_content)

        att = Attachment(
            file_url=relative_path, file_name=original_name, mime_type=mime_type,
            file_size=len(file_content), uploaded_by_id=user_id,
            linked_entity_type=entity_type, linked_entity_id=entity_id
        )
        self.db.add(att)
        self.db.commit()
        self.db.refresh(att)
        return att