# buildings.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.building import Building
from app.api.deps import require_permission
from pydantic import BaseModel

class BuildingCreate(BaseModel):
    address: str; name: str | None = None; territory_id: int | None = None

router = APIRouter()

@router.get("/")
def list_buildings(db: Session = Depends(get_db)):
    blds = db.execute(select(Building)).scalars().all()
    return [{"id": b.id, "address": b.address} for b in blds]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("object.manage"))])
def create_building(payload: BuildingCreate, db: Session = Depends(get_db)):
    b = Building(**payload.model_dump())
    db.add(b); db.commit(); db.refresh(b)
    return {"id": b.id, "address": b.address}