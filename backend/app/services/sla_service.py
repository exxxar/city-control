from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.problem import Problem
from app.models.sla_policy import SlaPolicy
from app.models.sla_timer import SlaTimer


class SlaService:
    def __init__(self, db: Session):
        self.db = db

    def _get_policy(self, problem: Problem) -> SlaPolicy | None:
        # Ищем политику по приоритету (можно расширить до поиска по категории/территории)
        stmt = select(SlaPolicy).where(SlaPolicy.priority_id == problem.priority_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def start_resolution_timer(self, problem: Problem):
        policy = self._get_policy(problem)
        if not policy:
            return

        now = datetime.now(timezone.utc)
        resolution_deadline = now + timedelta(minutes=policy.resolution_time_minutes)

        timer = SlaTimer(
            problem_id=problem.id, sla_policy_id=policy.id,
            reaction_deadline=now, resolution_deadline=resolution_deadline,
            is_reaction_met=True, is_resolution_met=False
        )
        self.db.add(timer)
        self.db.commit()

    def mark_resolution_met(self, problem: Problem):
        stmt = select(SlaTimer).where(SlaTimer.problem_id == problem.id, SlaTimer.is_resolution_met == False)
        timer = self.db.execute(stmt).scalar_one_or_none()
        if timer:
            timer.is_resolution_met = True
            self.db.commit()

    def get_overdue_problems(self) -> list[Problem]:
        now = datetime.now(timezone.utc)
        stmt = select(Problem).join(SlaTimer).where(
            SlaTimer.resolution_deadline < now, SlaTimer.is_resolution_met == False
        )
        return list(self.db.execute(stmt).scalars().all())