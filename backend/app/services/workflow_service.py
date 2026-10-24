from typing import Optional
from sqlalchemy.orm import Session
from app.models.problem import Problem, ProblemStatus
from app.models.user import User
from app.repositories.problem_repository import ProblemRepository
from app.services.sla_service import SlaService
from app.services.notification_service import NotificationService
from app.services.audit_service import AuditService


class WorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProblemRepository(db)
        self.sla_service = SlaService(db)
        self.notification_service = NotificationService(db)
        self.audit_service = AuditService(db)

    def change_status(self, problem: Problem, new_status: ProblemStatus, changed_by: User,
                      comment: Optional[str] = None):
        old_status = problem.status

        # Бизнес-правила переходов (упрощенно)
        if old_status == ProblemStatus.CLOSED:
            raise ValueError("Cannot change status of a closed problem")

        # Обновляем статус (репозиторий сам запишет историю)
        self.repo.update_status(problem, new_status, changed_by, comment)

        # Управление SLA
        if new_status == ProblemStatus.IN_PROGRESS:
            self.sla_service.start_resolution_timer(problem)
        elif new_status in [ProblemStatus.RESOLVED, ProblemStatus.CLOSED]:
            self.sla_service.mark_resolution_met(problem)

        # Уведомления
        self.notification_service.notify_status_change(problem, old_status, new_status, changed_by)

        # Аудит
        self.audit_service.log_action(
            changed_by.id, "change_status", "problem", problem.id,
            old_values={"status": old_status.value},
            new_values={"status": new_status.value, "comment": comment}
        )