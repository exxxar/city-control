from sqlalchemy.orm import Session
from app.models.map_layer import MapLayer
from app.models.map_zone import MapZone
from app.models.building import Building

class IndoorMapService:
    def __init__(self, db: Session):
        self.db = db

    def create_layer_for_building(self, building_id: int, name: str, file_url: str) -> MapLayer:
        layer = MapLayer(building_id=building_id, name=name, file_url=file_url)
        self.db.add(layer)
        self.db.commit()
        self.db.refresh(layer)
        return layer

    def draw_zone(self, layer_id: int, name: str, geometry: dict, room_id: int = None) -> MapZone:
        zone = MapZone(map_layer_id=layer_id, name=name, geometry=geometry, room_id=room_id)
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone