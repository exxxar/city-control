import enum
from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EventRequest(TimestampMixin, Base):
    __tablename__ = "event_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    event_type: Mapped[str] = mapped_column(String(100))  # subbotnik, exhibition, etc.
    description: Mapped[str | None] = mapped_column(Text)

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expected_participants: Mapped[int | None] = mapped_column(Integer)

    location_text: Mapped[str | None] = mapped_column(String(500))
    geo_tag_id: Mapped[int | None] = mapped_column(ForeignKey("geo_tags.id"))

    status: Mapped[EventStatus] = mapped_column(SQLEnum(EventStatus), default=EventStatus.DRAFT)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    responsible_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))