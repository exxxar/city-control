from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

# --- Municipal Object ---
class MunicipalObjectBase(BaseModel):
    name: str = Field(..., max_length=255)
    object_type: str = Field(..., max_length=100) # park, school, hospital
    territory_id: int

class MunicipalObjectCreate(MunicipalObjectBase):
    pass

class MunicipalObjectRead(MunicipalObjectBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Building ---
class BuildingBase(BaseModel):
    address: str = Field(..., max_length=500)
    name: Optional[str] = Field(None, max_length=255)
    object_id: Optional[int] = None
    territory_id: Optional[int] = None

class BuildingCreate(BuildingBase):
    pass

class BuildingRead(BuildingBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Floor & Room ---
class FloorRead(BaseModel):
    id: int
    building_id: int
    level: int
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class RoomRead(BaseModel):
    id: int
    floor_id: int
    name: str
    room_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)