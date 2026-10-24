from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Параметры пагинации, принимаемые из query-параметров."""
    page: int = Field(1, ge=1, description="Номер страницы")
    per_page: int = Field(20, ge=1, le=100, description="Элементов на странице")

class PaginatedResponse(BaseModel, Generic[T]):
    """Универсальная обертка для пагинированных списков."""
    items: List[T]
    total: int = Field(..., description="Общее количество элементов")
    page: int
    per_page: int
    pages: int = Field(..., description="Общее количество страниц")

class MessageResponse(BaseModel):
    """Простой ответ с сообщением."""
    message: str
    success: bool = True