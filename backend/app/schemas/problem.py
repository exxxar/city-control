# backend/app/schemas/problem.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.problem import ProblemStatus
from app.schemas.user import UserReadShort
from app.schemas.territory import TerritoryRead
from app.schemas.geo_tag import GeoTagRead


class ProblemBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    territory_id: Optional[int] = None
    geo_tag_id: Optional[int] = None
    category_id: Optional[int] = None
    priority_id: Optional[int] = None


class ProblemRead(ProblemBase):
    id: int
    public_id: str
    status: ProblemStatus

    rating: float
    confirmations_count: int

    # ВАЖНО: Эти поля могут быть NULL в базе, поэтому они Optional
    created_by_id: Optional[int] = None
    assigned_to_id: Optional[int] = None

    created_at: datetime
    updated_at: datetime

    # ВАЖНО: Вложенные объекты тоже могут быть None
    created_by: Optional[UserReadShort] = None
    assigned_to: Optional[UserReadShort] = None
    territory: Optional[TerritoryRead] = None
    geo_tag: Optional[GeoTagRead] = None

    # КРИТИЧЕСКИ ВАЖНО для Pydantic V2 + SQLAlchemy
    model_config = ConfigDict(from_attributes=True)