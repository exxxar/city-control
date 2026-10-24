# map_zone.py
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class MapZone(TimestampMixin, Base):
    __tablename__ = "map_zones"
    id: Mapped[int] = mapped_column(primary_key=True)
    map_layer_id: Mapped[int] = mapped_column(ForeignKey("map_layers.id"))
    room_id: Mapped[int | None] = mapped_column(ForeignKey("rooms.id"))
    name: Mapped[str] = mapped_column(String(255))
    geometry: Mapped[dict] = mapped_column(JSON) # GeoJSON polygon