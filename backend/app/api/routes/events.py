from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from app.db.session import get_db
from app.models.event_request import EventRequest, EventStatus
from app.models.user import User
from app.api.deps import get_current_user, require_permission
from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str; event_type: str; start_date: datetime
    description: str | None = None; location_text: str | None = None

router = APIRouter()

@router.get("/")
def list_events(db: Session = Depends(get_db)):
    items = db.execute(select(EventRequest)).scalars().all()
    return [{"id": e.id, "title": e.title, "type": e.event_type, "status": e.status.value, "date": e.start_date.isoformat()} for e in items]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("event.create"))])
def create_event(payload: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    event = EventRequest(**payload.model_dump(), created_by_id=current_user.id, status=EventStatus.DRAFT)
    db.add(event); db.commit(); db.refresh(event)
    return {"id": event.id, "title": event.title}

@router.patch("/{event_id}/status", dependencies=[Depends(require_permission("event.approve"))])
def update_event_status(event_id: int, new_status: EventStatus, db: Session = Depends(get_db)):
    event = db.get(EventRequest, event_id)
    if not event: raise HTTPException(404, "Event not found")
    event.status = new_status
    db.commit()
    return {"id": event.id, "status": event.status.value}