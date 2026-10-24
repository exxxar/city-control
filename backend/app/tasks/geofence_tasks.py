# backend/app/tasks/geofence_tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from app.db.session import SessionLocal
from app.models.user import User
from app.models.geo_tag import GeoTag, GeoTagType
from app.models.problem import Problem, ProblemStatus
from app.models.notification import Notification, NotificationType
from app.integrations.pusher.client import pusher_client
from app.integrations.pusher.events import PusherEvents, PusherChannels
from loguru import logger


@shared_task
def check_user_geofence(user_id: int, latitude: float, longitude: float):
    """
    Проверяет попадание пользователя в зоны активных проблем.
    Вызывается клиентом (PWA/Android) при обновлении геолокации.
    """
    db: Session = SessionLocal()
    try:
        user = db.get(User, user_id)
        if not user:
            return

        # Находим все активные GPS-метки и полигоны
        stmt = select(GeoTag).where(
            GeoTag.active == True,
            GeoTag.notification_enabled == True,
            GeoTag.type.in_([GeoTagType.GPS, GeoTagType.POLYGON])
        )
        tags = db.execute(stmt).scalars().all()

        triggered_problems = []

        for tag in tags:
            if tag.type == GeoTagType.GPS and tag.latitude and tag.longitude:
                # Грубая проверка расстояния (в реальности - формула Хаверсина или PostGIS)
                dist = ((tag.latitude - latitude) ** 2 + (tag.longitude - longitude) ** 2) ** 0.5 * 111000
                if dist <= (tag.notification_radius or 100):
                    # Ищем связанные проблемы
                    problems = db.execute(
                        select(Problem).where(
                            Problem.geo_tag_id == tag.id,
                            Problem.status.in_([ProblemStatus.NEW, ProblemStatus.CONFIRMED, ProblemStatus.IN_PROGRESS])
                        )
                    ).scalars().all()
                    triggered_problems.extend(problems)

        if triggered_problems:
            # Группируем уведомления, чтобы не спамить
            count = len(triggered_problems)
            first_problem = triggered_problems[0]

            notif = Notification(
                user_id=user_id,
                type=NotificationType.GEO_ZONE_ENTRY,
                title=f"Рядом {count} проблем(ы)",
                body=f"Вы находитесь в зоне активных обращений. Ближайшее: '{first_problem.title}'",
                linked_entity_type="problem",
                linked_entity_id=first_problem.id
            )
            db.add(notif)
            db.commit()

            # Отправляем Real-Time событие через Pusher
            pusher_client.trigger(
                PusherChannels.user_channel(user_id),
                PusherEvents.GEO_ZONE_ENTRY,
                {
                    "notification_id": notif.id,
                    "problems_count": count,
                    "latitude": latitude,
                    "longitude": longitude
                }
            )
            logger.info(f"Geofence triggered for user {user_id}: {count} problems nearby")

    except Exception as e:
        logger.error(f"Error in geofence task for user {user_id}: {e}")
    finally:
        db.close()