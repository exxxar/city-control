from pydantic import BaseModel, field_validator
from typing import List, Optional
import json

class IssueCategoryRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    type: int
    variants: List[str] = []

    @field_validator('variants', mode='before')
    @classmethod
    def parse_variants(cls, v):
        """Парсим JSON-строку из БД в массив строк"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        if isinstance(v, list):
            return v
        return []

    class Config:
        from_attributes = True