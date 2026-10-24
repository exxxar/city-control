# backend/app/models/event.py
import enum
from datetime import datetime, date
from sqlalchemy import String, Text, Date, Integer, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class EventStatus(str, enum.Enum):
    PENDING = "pending"  # На согласовании
    APPROVED = "approved"  # Согласовано
    REJECTED = "rejected"  # Отклонено
    COMPLETED = "completed"  # Завершено
    CANCELLED = "cancelled"  # Отменено


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    event_date: Mapped[date | None] = mapped_column(Date)

    organizer_name: Mapped[str] = mapped_column(String(255))
    organizer_phone: Mapped[str | None] = mapped_column(String(50))

    target_audience: Mapped[str | None] = mapped_column(String(255))
    participants_count: Mapped[int] = mapped_column(Integer, default=0)

    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus, values_callable=lambda x: [e.value for e in x]),
        default=EventStatus.PENDING
    )

    reject_reason: Mapped[str | None] = mapped_column(Text)

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by_id])