# backend/app/db/seed/initial_initiatives.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.initiative import Initiative, InitiativeStatus
from app.models.initiative_support import InitiativeSupport
from app.models.user import User
from app.models.category import Category
from app.models.territory import Territory


def seed_initiatives(db: Session):
    print("Seeding initiatives...")

    if db.execute(select(Initiative)).first():
        print("Initiatives already exist, skipping.")
        return

    citizen = db.execute(select(User).where(User.email == "citizen@city.local")).scalar_one()
    admin = db.execute(select(User).where(User.email == "admin@city.local")).scalar_one()

    podolsk = db.execute(select(Territory).where(Territory.code == "PODOLSK")).scalar_one()

    initiatives_data = [
        {
            "title": "Установить детскую площадку во дворе",
            "description": "Предлагаю установить современную детскую площадку с безопасным покрытием.",
            "status": InitiativeStatus.UNDER_REVIEW,
            "territory_id": podolsk.id,
            "created_by_id": citizen.id,
            "support_count": 15
        },
        {
            "title": "Организовать велодорожку",
            "description": "Необходима велодорожка от парка до центра города.",
            "status": InitiativeStatus.ACCEPTED,
            "territory_id": podolsk.id,
            "created_by_id": citizen.id,
            "support_count": 42
        },
        {
            "title": "Высадить деревья на улице",
            "description": "Предлагаю высадить молодые деревья вдоль улицы для улучшения экологии.",
            "status": InitiativeStatus.NEW,
            "territory_id": podolsk.id,
            "created_by_id": citizen.id,
            "support_count": 3
        }
    ]

    for data in initiatives_data:
        init = Initiative(**data)
        db.add(init)

    db.commit()

    # Добавляем поддержки от разных пользователей
    users = db.execute(select(User)).scalars().all()
    initiatives = db.execute(select(Initiative)).scalars().all()

    for init in initiatives:
        # Добавляем поддержку от всех пользователей, кроме автора
        for user in users:
            if user.id != init.created_by_id:
                support = InitiativeSupport(initiative_id=init.id, user_id=user.id)
                db.add(support)

    db.commit()
    print("Initiatives seeded.")