from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.db.session import get_db
from app.models.notification import Notification
from app.models.user import User
from app.api.deps import get_current_user
from pydantic import BaseModel

class MarkReadRequest(BaseModel):
    ids: list[int]

router = APIRouter()

@router.get("/")
def my_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifs = db.execute(select(Notification).where(Notification.user_id == current_user.id).limit(50)).scalars().all()
    return [{"id": n.id, "title": n.title, "type": n.type.value, "is_read": n.is_read} for n in notifs]

@router.patch("/read")
def mark_as_read(payload: MarkReadRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(update(Notification).where(
        Notification.id.in_(payload.ids), Notification.user_id == current_user.id
    ).values(is_read=True))
    db.commit()
    return {"message": "Marked as read"}