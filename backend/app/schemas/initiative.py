from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.initiative import InitiativeStatus
from app.schemas.user import UserReadShort


class InitiativeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    territory_id: Optional[int] = None
    geo_tag_id: Optional[int] = None
    category_id: Optional[int] = None


class InitiativeCreate(InitiativeBase):
    pass


class InitiativeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[InitiativeStatus] = None


class InitiativeRead(InitiativeBase):
    id: int
    status: InitiativeStatus
    support_count: int
    created_by_id: int
    created_by: Optional[UserReadShort] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)