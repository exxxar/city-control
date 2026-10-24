from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone

from app.db.session import SessionLocal
from app.models.sla_timer import SlaTimer
from app.models.problem import Problem
from app.models.notification import Notification, NotificationType
from app.integrations.pusher.client import pusher_client
from loguru import logger


@shared_task
def check_sla_overdue():
    """Находит проблемы, у которых истек SLA, и отправляет уведомления."""
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        # Ищем таймеры, где дедлайн прошел, но галочка не стоит
        stmt = select(SlaTimer).where(
            SlaTimer.resolution_deadline < now,
            SlaTimer.is_resolution_met == False
        )
        overdue_timers = db.execute(stmt).scalars().all()

        for timer in overdue_timers:
            problem = db.get(Problem, timer.problem_id)
            if not problem:
                continue

            # Создаем уведомление для исполнителя и руководителя
            target_user_ids = set()
            if problem.assigned_to_id:
                target_user_ids.add(problem.assigned_to_id)
            # TODO: Добавить руководителя органа

            for user_id in target_user_ids:
                notif = Notification(
                    user_id=user_id,
                    type=NotificationType.SLA_WARNING,
                    title="⚠️ Нарушение SLA",
                    body=f"Срок устранения проблемы '{problem.title}' истек.",
                    linked_entity_type="problem",
                    linked_entity_id=problem.id
                )
                db.add(notif)

                # Отправляем Pusher событие
                pusher_client.trigger(
                    f"private-user-{user_id}",
                    "sla.overdue",
                    {"problem_id": problem.id, "title": problem.title}
                )

            logger.warning(f"SLA overdue for problem {problem.public_id}")

        db.commit()
    except Exception as e:
        logger.error(f"Error checking SLA: {e}")
    finally:
        db.close()