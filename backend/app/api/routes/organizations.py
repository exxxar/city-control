# organizations.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.executor_organization import ExecutorOrganization
from app.api.deps import require_permission
from pydantic import BaseModel

class OrgCreate(BaseModel):
    name: str; email: str | None = None; territory_id: int | None = None

router = APIRouter()

@router.get("/")
def list_orgs(db: Session = Depends(get_db)):
    orgs = db.execute(select(ExecutorOrganization)).scalars().all()
    return [{"id": o.id, "name": o.name, "email": o.email} for o in orgs]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("admin.full_access"))])
def create_org(payload: OrgCreate, db: Session = Depends(get_db)):
    org = ExecutorOrganization(**payload.model_dump())
    db.add(org); db.commit(); db.refresh(org)
    return {"id": org.id, "name": org.name}