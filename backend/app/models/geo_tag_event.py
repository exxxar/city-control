# backend/app/models/geo_tag_event.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class GeoTagEvent(TimestampMixin, Base):
    __tablename__ = "geo_tag_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    geo_tag_id: Mapped[int] = mapped_column(ForeignKey("geo_tags.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    event_type: Mapped[str] = mapped_column(String(50))  # enter, exit, scan

    # ПЕРЕИМЕНОВАНО: metadata -> event_metadata (так как metadata зарезервировано в SQLAlchemy)
    event_metadata: Mapped[str | None] = mapped_column(String(500))