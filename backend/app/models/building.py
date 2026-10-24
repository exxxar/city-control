# building.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class Building(TimestampMixin, Base):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(primary_key=True)
    object_id: Mapped[int | None] = mapped_column(ForeignKey("municipal_objects.id"))
    territory_id: Mapped[int | None] = mapped_column(ForeignKey("territories.id"))
    address: Mapped[str] = mapped_column(String(500))
    name: Mapped[str | None] = mapped_column(String(255))