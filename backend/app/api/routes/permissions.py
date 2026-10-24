# permissions.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.permission import Permission
from app.api.deps import require_permission

router = APIRouter()

@router.get("/", dependencies=[Depends(require_permission("role.manage"))])
def list_permissions(db: Session = Depends(get_db)):
    perms = db.execute(select(Permission)).scalars().all()
    return [{"id": p.id, "codename": p.codename, "name": p.name} for p in perms]