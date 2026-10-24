from datetime import datetime
from sqlalchemy.orm import Session
from app.models.event_request import EventRequest, EventStatus
from app.models.user import User

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create_event_request(self, user: User, title: str, event_type: str, start_date: datetime, location_text: str) -> EventRequest:
        event = EventRequest(
            title=title, event_type=event_type, start_date=start_date,
            location_text=location_text, created_by_id=user.id, status=EventStatus.DRAFT
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def approve_event(self, event_id: int, responsible_user_id: int):
        event = self.db.get(EventRequest, event_id)
        if event:
            event.status = EventStatus.APPROVED
            event.responsible_user_id = responsible_user_id
            self.db.commit()