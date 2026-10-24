from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.attachment import Attachment
from app.models.user import User
from app.api.deps import get_current_user
import uuid

router = APIRouter()


@router.post("/", status_code=201)
async def upload_attachment(
        file: UploadFile = File(...),
        linked_entity_type: str = "problem",
        linked_entity_id: int = 1,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Мок сохранения файла
    file_url = f"/storage/uploads/originals/{uuid.uuid4()}_{file.filename}"

    att = Attachment(
        file_url=file_url, file_name=file.filename, mime_type=file.content_type or "application/octet-stream",
        file_size=0, uploaded_by_id=current_user.id,
        linked_entity_type=linked_entity_type, linked_entity_id=linked_entity_id
    )
    db.add(att);
    db.commit();
    db.refresh(att)
    return {"id": att.id, "url": att.url, "name": att.file_name}