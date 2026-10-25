# backend/app/api/routes/categories.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db

# Убедитесь, что имя модели совпадает с вашим (IssueCategory или Category)
from app.models.issue_category import IssueCategory

router = APIRouter()


@router.get("")
def get_categories(
        type: int = Query(0, description="Тип категории: 0 - проблемы, 1 - решения, 2 - трудности"),
        db: Session = Depends(get_db)
):
    """
    Возвращает список категорий. По умолчанию возвращает категории проблем (type=0).
    """
    query = db.query(IssueCategory).filter(IssueCategory.type == type)
    categories = query.all()

    return [
        {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "icon": cat.icon,
            "type": cat.type
        }
        for cat in categories
    ]