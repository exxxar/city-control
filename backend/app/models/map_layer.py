# map_layer.py
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class MapLayer(TimestampMixin, Base):
    __tablename__ = "map_layers"
    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    floor_id: Mapped[int | None] = mapped_column(ForeignKey("floors.id"))
    name: Mapped[str] = mapped_column(String(255))
    file_url: Mapped[str] = mapped_column(String(500))
    bounds: Mapped[dict | None] = mapped_column(JSON) # GeoJSON bounds