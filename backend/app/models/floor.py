# backend/app/models/floor.py
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class Floor(TimestampMixin, Base):
    __tablename__ = "floors"

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    level: Mapped[int] = mapped_column(Integer)
    name: Mapped[str | None] = mapped_column(String(50))