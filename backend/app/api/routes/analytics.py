from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.problem import Problem, ProblemStatus
from app.api.deps import require_permission

router = APIRouter()


@router.get("/dashboard", dependencies=[Depends(require_permission("analytics.view"))])
def get_dashboard_kpi(db: Session = Depends(get_db)):
    total = db.execute(select(func.count(Problem.id))).scalar()
    new = db.execute(select(func.count(Problem.id)).where(Problem.status == ProblemStatus.NEW)).scalar()
    in_progress = db.execute(select(func.count(Problem.id)).where(Problem.status == ProblemStatus.IN_PROGRESS)).scalar()

    return {
        "total_problems": total or 0,
        "new_problems": new or 0,
        "in_progress": in_progress or 0,
        "avg_resolution_hours": 42.5  # Мок
    }


@router.get("/heatmap", dependencies=[Depends(require_permission("analytics.view"))])
def get_heatmap(db: Session = Depends(get_db)):
    # Мок данных для тепловой карты
    return {"points": [{"lat": 55.1, "lng": 37.1, "weight": 10}, {"lat": 55.2, "lng": 37.2, "weight": 5}]}