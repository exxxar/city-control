# roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.admin import CategoryRead # Используем как базу или создадим RoleRead inline
from pydantic import BaseModel
from app.api.deps import require_permission

class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    permission_ids: list[int] = []

router = APIRouter()

@router.get("/", response_model=list[dict], dependencies=[Depends(require_permission("role.manage"))])
def list_roles(db: Session = Depends(get_db)):
    roles = db.execute(select(Role)).scalars().all()
    return [{"id": r.id, "name": r.name, "description": r.description, "permissions": [p.codename for p in r.permissions]} for r in roles]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("role.manage"))])
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    role = Role(name=payload.name, description=payload.description)
    if payload.permission_ids:
        perms = db.execute(select(Permission).where(Permission.id.in_(payload.permission_ids))).scalars().all()
        role.permissions = list(perms)
    db.add(role); db.commit(); db.refresh(role)
    return {"id": role.id, "name": role.name}