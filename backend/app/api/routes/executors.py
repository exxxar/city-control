# executors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.executor import Executor
from app.models.user import User
from app.api.deps import require_permission
from pydantic import BaseModel

class ExecutorAssign(BaseModel):
    user_id: int; organization_id: int; is_primary: bool = False

router = APIRouter()

@router.get("/", dependencies=[Depends(require_permission("user.view"))])
def list_executors(db: Session = Depends(get_db)):
    execs = db.execute(select(Executor)).scalars().all()
    return [{"id": e.id, "user_id": e.user_id, "org_id": e.organization_id} for e in execs]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("user.manage"))])
def assign_executor(payload: ExecutorAssign, db: Session = Depends(get_db)):
    if not db.get(User, payload.user_id): raise HTTPException(404, "User not found")
    exec = Executor(**payload.model_dump())
    db.add(exec); db.commit(); db.refresh(exec)
    return {"id": exec.id, "message": "Executor assigned"}