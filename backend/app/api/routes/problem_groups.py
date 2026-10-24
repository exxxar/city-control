# problem_groups.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.problem_group import ProblemGroup
from app.api.deps import require_permission

router = APIRouter()

@router.get("/", dependencies=[Depends(require_permission("problem.view_all"))])
def list_groups(db: Session = Depends(get_db)):
    groups = db.execute(select(ProblemGroup)).scalars().all()
    return [{"id": g.id, "title": g.title, "total": g.total_problems} for g in groups]