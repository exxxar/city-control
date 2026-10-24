from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.help_format import HelpFormat
from app.schemas.help_format import HelpFormatRead

router = APIRouter()

@router.get("/help-formats", response_model=List[HelpFormatRead], summary="Получить форматы помощи")
def get_help_formats(db: Session = Depends(get_db)):
    """
    Возвращает справочник форматов помощи для мероприятий.
    """
    return db.query(HelpFormat).order_by(HelpFormat.id).all()