# objects.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.municipal_object import MunicipalObject
from app.api.deps import require_permission
from pydantic import BaseModel

class ObjectCreate(BaseModel):
    name: str; object_type: str; territory_id: int

router = APIRouter()

@router.get("/")
def list_objects(db: Session = Depends(get_db)):
    objs = db.execute(select(MunicipalObject)).scalars().all()
    return [{"id": o.id, "name": o.name, "type": o.object_type} for o in objs]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("object.manage"))])
def create_object(payload: ObjectCreate, db: Session = Depends(get_db)):
    obj = MunicipalObject(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return {"id": obj.id, "name": obj.name}