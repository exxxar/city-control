from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.initiative import Initiative, InitiativeStatus
from app.models.initiative_support import InitiativeSupport
from app.models.user import User
from app.api.deps import get_current_user, require_permission
from pydantic import BaseModel


class InitiativeCreate(BaseModel):
    title: str;
    description: str | None = None
    territory_id: int | None = None;
    category_id: int | None = None


router = APIRouter()


@router.get("/")
def list_initiatives(db: Session = Depends(get_db)):
    items = db.execute(select(Initiative)).scalars().all()
    return [{"id": i.id, "title": i.title, "status": i.status.value, "support_count": i.support_count} for i in items]


@router.post("/", status_code=201, dependencies=[Depends(require_permission("initiative.create"))])
def create_initiative(payload: InitiativeCreate, current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    init = Initiative(**payload.model_dump(), created_by_id=current_user.id, status=InitiativeStatus.NEW)
    db.add(init);
    db.commit();
    db.refresh(init)
    return {"id": init.id, "title": init.title, "status": init.status.value}


@router.post("/{init_id}/support", status_code=201)
def support_initiative(init_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    init = db.get(Initiative, init_id)
    if not init: raise HTTPException(404, "Initiative not found")

    # Проверяем, не поддерживал ли уже
    exists = db.execute(select(InitiativeSupport).where(
        InitiativeSupport.initiative_id == init_id, InitiativeSupport.user_id == current_user.id
    )).scalar_one_or_none()
    if exists: raise HTTPException(400, "Already supported")

    db.add(InitiativeSupport(initiative_id=init_id, user_id=current_user.id))
    init.support_count += 1
    db.commit()
    return {"message": "Supported", "total": init.support_count}