# backend/app/api/routes/problems.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.db.session import get_db
from app.models.problem import Problem, ProblemStatus
from app.schemas.problem import ProblemRead

router = APIRouter()


@router.get("/", response_model=List[ProblemRead])
def list_problems(
        status: Optional[ProblemStatus] = Query(None),
        db: Session = Depends(get_db)
):
    stmt = select(Problem)
    if status:
        stmt = stmt.where(Problem.status == status)

    # Возвращаем список ORM-объектов. FastAPI сам превратит их в ProblemRead
    # благодаря from_attributes=True в схеме
    problems = db.execute(stmt.limit(100)).scalars().all()
    return problems