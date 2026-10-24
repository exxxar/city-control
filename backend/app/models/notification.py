# notification.py
import enum
from sqlalchemy import String, Text, Integer, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class NotificationType(str, enum.Enum):
    STATUS_CHANGE = "status_change"
    NEW_MESSAGE = "new_message"
    SLA_WARNING = "sla_warning"
    GEO_ZONE_ENTRY = "geo_zone_entry"
    SYSTEM = "system"


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[NotificationType] = mapped_column(SQLEnum(NotificationType))

    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str | None] = mapped_column(Text)

    linked_entity_type: Mapped[str | None] = mapped_column(String(50))
    linked_entity_id: Mapped[int | None] = mapped_column(Integer)

    is_read: Mapped[bool] = mapped_column(Boolean, default=False)