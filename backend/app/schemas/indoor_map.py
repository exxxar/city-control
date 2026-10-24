from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class MapLayerBase(BaseModel):
    name: str = Field(..., max_length=255)
    building_id: int
    floor_id: Optional[int] = None
    file_url: str
    bounds: Optional[Dict[str, Any]] = None # GeoJSON bounds

class MapLayerCreate(MapLayerBase):
    pass

class MapLayerRead(MapLayerBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MapZoneBase(BaseModel):
    name: str = Field(..., max_length=255)
    map_layer_id: int
    room_id: Optional[int] = None
    geometry: Dict[str, Any] # GeoJSON polygon

class MapZoneCreate(MapZoneBase):
    pass

class MapZoneRead(MapZoneBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)