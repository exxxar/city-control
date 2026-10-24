# municipal_object.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class MunicipalObject(TimestampMixin, Base):
    __tablename__ = "municipal_objects"
    id: Mapped[int] = mapped_column(primary_key=True)
    territory_id: Mapped[int] = mapped_column(ForeignKey("territories.id"))
    name: Mapped[str] = mapped_column(String(255))
    object_type: Mapped[str] = mapped_column(String(100)) # park, school, etc.