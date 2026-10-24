from typing import TypeVar, Generic, List
from pydantic import BaseModel, Field
from fastapi import Query

T = TypeVar('T')

class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Номер страницы"),
        per_page: int = Query(20, ge=1, le=100, description="Элементов на странице")
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    pages: int = Field(..., description="Общее количество страниц")

    @classmethod
    def create(cls, items: List[T], total: int, page: int, per_page: int):
        pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        return cls(items=items, total=total, page=page, per_page=per_page, pages=pages)