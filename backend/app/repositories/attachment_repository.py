# backend/app/repositories/attachment_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.attachment import Attachment

class AttachmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, attachment_id: int) -> Optional[Attachment]:
        return self.db.get(Attachment, attachment_id)

    def list_by_entity(self, entity_type: str, entity_id: int) -> List[Attachment]:
        stmt = select(Attachment).where(
            Attachment.linked_entity_type == entity_type,
            Attachment.linked_entity_id == entity_id
        ).order_by(Attachment.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def create(self, attachment: Attachment) -> Attachment:
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment