# backend/app/db/seed/initial_notifications.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.notification import Notification, NotificationType
from app.models.user import User
from app.models.problem import Problem


def seed_notifications(db: Session):
    print("Seeding notifications...")

    if db.execute(select(Notification)).first():
        print("Notifications already exist, skipping.")
        return

    citizen = db.execute(select(User).where(User.email == "citizen@city.local")).scalar_one()
    executor = db.execute(select(User).where(User.email == "executor@city.local")).scalar_one()
    admin = db.execute(select(User).where(User.email == "admin@city.local")).scalar_one()

    problem = db.execute(select(Problem)).first()
    if not problem:
        print("No problems found, skipping notifications.")
        return
    problem = problem[0]

    notifications_data = [
        {
            "user_id": citizen.id,
            "type": NotificationType.STATUS_CHANGE,
            "title": "Статус проблемы изменён",
            "body": f"Ваша проблема '{problem.title}' переведена в статус 'В работе'",
            "linked_entity_type": "problem",
            "linked_entity_id": problem.id,
            "is_read": False
        },
        {
            "user_id": executor.id,
            "type": NotificationType.NEW_MESSAGE,
            "title": "Новое сообщение в чате",
            "body": f"Пользователь оставил комментарий к проблеме '{problem.title}'",
            "linked_entity_type": "problem",
            "linked_entity_id": problem.id,
            "is_read": False
        },
        {
            "user_id": admin.id,
            "type": NotificationType.SYSTEM,
            "title": "Новая проблема в системе",
            "body": f"Зарегистрирована новая проблема: '{problem.title}'",
            "linked_entity_type": "problem",
            "linked_entity_id": problem.id,
            "is_read": True
        }
    ]

    for data in notifications_data:
        notif = Notification(**data)
        db.add(notif)

    db.commit()
    print("Notifications seeded.")