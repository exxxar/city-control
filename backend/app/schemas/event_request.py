from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.event_request import EventStatus
from app.schemas.user import UserReadShort


class EventRequestBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    event_type: str = Field(..., max_length=100)  # subbotnik, exhibition
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    expected_participants: Optional[int] = Field(None, ge=1)
    location_text: Optional[str] = None
    geo_tag_id: Optional[int] = None


class EventRequestCreate(EventRequestBase):
    pass


class EventRequestUpdate(BaseModel):
    status: Optional[EventStatus] = None
    responsible_user_id: Optional[int] = None
    # ... другие поля для редактирования


class EventRequestRead(EventRequestBase):
    id: int
    status: EventStatus
    created_by_id: int
    responsible_user_id: Optional[int] = None

    created_by: Optional[UserReadShort] = None
    responsible_user: Optional[UserReadShort] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)