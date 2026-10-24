from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.territory import TerritoryLevel


class TerritoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    level: TerritoryLevel
    code: Optional[str] = Field(None, max_length=50)
    parent_id: Optional[int] = None


class TerritoryCreate(TerritoryBase):
    pass


class TerritoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = None
    parent_id: Optional[int] = None


class TerritoryRead(TerritoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TerritoryTree(TerritoryRead):
    """Схема для возврата дерева территорий (с детьми)."""
    children: List["TerritoryTree"] = []

    model_config = ConfigDict(from_attributes=True)


# Разрыв рекурсии для Pydantic
TerritoryTree.model_rebuild()