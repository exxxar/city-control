from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from app.models.geo_tag import GeoTagType


class GeoTagBase(BaseModel):
    type: GeoTagType
    active: bool = True
    notification_enabled: bool = True

    # GPS
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[float] = Field(None, ge=0, description="Радиус в метрах")
    notification_radius: Optional[float] = Field(None, ge=0)

    # Polygon / Geometry (GeoJSON)
    geometry: Optional[Dict[str, Any]] = None

    # Indoor
    building_id: Optional[int] = None
    floor_id: Optional[int] = None
    room_id: Optional[int] = None


class GeoTagCreate(GeoTagBase):
    pass


class GeoTagUpdate(BaseModel):
    active: Optional[bool] = None
    notification_enabled: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[float] = None
    notification_radius: Optional[float] = None
    geometry: Optional[Dict[str, Any]] = None
    building_id: Optional[int] = None
    floor_id: Optional[int] = None
    room_id: Optional[int] = None


class GeoTagRead(GeoTagBase):
    id: int
    qr_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)