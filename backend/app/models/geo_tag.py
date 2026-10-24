# geo_tag.py
import enum, uuid
from sqlalchemy import String, Float, Boolean, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class GeoTagType(str, enum.Enum):
    GPS = "gps"; POLYGON = "polygon"; QR = "qr"; INDOOR = "indoor"

class GeoTag(TimestampMixin, Base):
    __tablename__ = "geo_tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[GeoTagType] = mapped_column(SQLEnum(GeoTagType))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    radius: Mapped[float | None] = mapped_column(Float)
    geometry: Mapped[dict | None] = mapped_column(JSON)
    building_id: Mapped[int | None] = mapped_column(ForeignKey("buildings.id"))
    floor_id: Mapped[int | None] = mapped_column(ForeignKey("floors.id"))
    room_id: Mapped[int | None] = mapped_column(ForeignKey("rooms.id"))
    qr_token: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    notification_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    notification_radius: Mapped[float | None] = mapped_column(Float)