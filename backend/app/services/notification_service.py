from typing import List
from sqlalchemy.orm import Session
from app.models.problem import Problem, ProblemStatus
from app.models.user import User
from app.models.notification import Notification, NotificationType
from app.models.geo_tag import GeoTag


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def _create_notification(self, user_id: int, type: NotificationType, title: str, body: str, entity_type: str = None,
                             entity_id: int = None):
        notif = Notification(
            user_id=user_id, type=type, title=title, body=body,
            linked_entity_type=entity_type, linked_entity_id=entity_id
        )
        self.db.add(notif)
        self.db.commit()
        # TODO: Вызвать pusher_service.trigger(...) и email_service.send(...)

    def notify_new_problem(self, problem: Problem):
        # Упрощенно: здесь должен быть запрос пользователей с правом problem.moderate
        pass

    def notify_problem_confirmed(self, problem: Problem, user: User):
        self._create_notification(
            user_id=problem.created_by_id, type=NotificationType.STATUS_CHANGE,
            title="Ваша проблема подтверждена",
            body=f"Пользователь {user.full_name} подтвердил проблему '{problem.title}'",
            entity_type="problem", entity_id=problem.id
        )

    def notify_status_change(self, problem: Problem, old_status: ProblemStatus, new_status: ProblemStatus,
                             changed_by: User):
        target_users = {problem.created_by_id}
        if problem.assigned_to_id: target_users.add(problem.assigned_to_id)

        for uid in target_users:
            if uid == changed_by.id: continue
            self._create_notification(
                user_id=uid, type=NotificationType.STATUS_CHANGE,
                title="Статус проблемы изменен",
                body=f"Проблема '{problem.title}' переведена в статус '{new_status.value}'",
                entity_type="problem", entity_id=problem.id
            )

    def notify_geo_zone_entry(self, user_id: int, tags: List[GeoTag]):
        count = len(tags)
        self._create_notification(
            user_id=user_id, type=NotificationType.GEO_ZONE_ENTRY,
            title="Рядом есть проблемы",
            body=f"Вы находитесь в зоне {count} активных проблем.",
            entity_type="geotag", entity_id=tags[0].id
        )