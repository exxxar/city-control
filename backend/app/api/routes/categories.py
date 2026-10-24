from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.issue_category import IssueCategory
from app.schemas.issue_category import IssueCategoryRead

router = APIRouter()

@router.get("/issue-categories", response_model=List[IssueCategoryRead], summary="Получить справочник категорий")
def get_issue_categories(
    type: int | None = None,  # Опциональный фильтр по типу (0, 1, 2)
    db: Session = Depends(get_db)
):
    """
    Возвращает справочник категорий проблем, решений и трудностей.
    Можно фильтровать по параметру type.
    """
    query = db.query(IssueCategory)

    if type is not None:
        query = query.filter(IssueCategory.type == type)

    categories = query.order_by(IssueCategory.type, IssueCategory.id).all()
    return categories