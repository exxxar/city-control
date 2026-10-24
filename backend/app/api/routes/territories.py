# territories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.territory import Territory, TerritoryLevel
from app.api.deps import require_permission
from pydantic import BaseModel

class TerritoryCreate(BaseModel):
    name: str; level: TerritoryLevel; code: str; parent_id: int | None = None

router = APIRouter()

@router.get("/tree")
def get_territory_tree(db: Session = Depends(get_db)):
    # Упрощенный плоский список для старта (дерево строится на фронте или через рекурсию)
    territories = db.execute(select(Territory)).scalars().all()
    return [{"id": t.id, "name": t.name, "level": t.level.value, "parent_id": t.parent_id} for t in territories]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("territory.manage"))])
def create_territory(payload: TerritoryCreate, db: Session = Depends(get_db)):
    t = Territory(**payload.model_dump())
    db.add(t); db.commit(); db.refresh(t)
    return {"id": t.id, "name": t.name}