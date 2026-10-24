from sqlalchemy.orm import Session
from app.models.problem import Problem, ProblemStatus
from app.models.responsibility_transfer import ResponsibilityTransfer
from app.models.user import User
from app.services.notification_service import NotificationService


class ResponsibilityService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)

    def transfer_problem(self, problem: Problem, to_user: User, from_user: User, reason: str = None):
        """Передает проблему другому исполнителю/органу."""
        transfer = ResponsibilityTransfer(
            problem_id=problem.id, from_user_id=from_user.id, to_user_id=to_user.id,
            reason=reason, transferred_by_id=from_user.id
        )
        self.db.add(transfer)

        problem.assigned_to_id = to_user.id
        problem.status = ProblemStatus.TRANSFERRED

        self.db.commit()
        self.notification_service.notify_status_change(problem, ProblemStatus.IN_PROGRESS, ProblemStatus.TRANSFERRED,
                                                       from_user)