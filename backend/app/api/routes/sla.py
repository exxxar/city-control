from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.sla_policy import SlaPolicy
from app.models.sla_timer import SlaTimer
from app.api.deps import require_permission
from pydantic import BaseModel

class PolicyCreate(BaseModel):
    name: str; priority_id: int | None = None
    reaction_time_minutes: int; resolution_time_minutes: int

router = APIRouter()

@router.get("/policies", dependencies=[Depends(require_permission("sla.manage"))])
def list_policies(db: Session = Depends(get_db)):
    policies = db.execute(select(SlaPolicy)).scalars().all()
    return [{"id": p.id, "name": p.name, "reaction": p.reaction_time_minutes} for p in policies]

@router.post("/policies", status_code=201, dependencies=[Depends(require_permission("sla.manage"))])
def create_policy(payload: PolicyCreate, db: Session = Depends(get_db)):
    policy = SlaPolicy(**payload.model_dump())
    db.add(policy); db.commit(); db.refresh(policy)
    return {"id": policy.id, "name": policy.name}

@router.get("/timers/overdue", dependencies=[Depends(require_permission("problem.view_all"))])
def get_overdue_timers(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    # Находим таймеры, где дедлайн прошел, а галочка не стоит
    timers = db.execute(select(SlaTimer).where(
        SlaTimer.resolution_deadline < now, SlaTimer.is_resolution_met == False
    )).scalars().all()
    return [{"id": t.id, "problem_id": t.problem_id, "deadline": t.resolution_deadline.isoformat()} for t in timers]