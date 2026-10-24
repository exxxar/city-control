# backend/app/db/seed/initial_events.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.event_request import EventRequest, EventStatus
from app.models.user import User
from app.models.territory import Territory


def seed_events(db: Session):
    print("Seeding events...")

    if db.execute(select(EventRequest)).first():
        print("Events already exist, skipping.")
        return

    citizen = db.execute(select(User).where(User.email == "citizen@city.local")).scalar_one()
    admin = db.execute(select(User).where(User.email == "admin@city.local")).scalar_one()

    podolsk = db.execute(select(Territory).where(Territory.code == "PODOLSK")).scalar_one()

    events_data = [
        {
            "title": "Субботник в парке",
            "event_type": "subbotnik",
            "description": "Приглашаем всех на уборку парка.",
            "start_date": datetime.now() + timedelta(days=7),
            "end_date": datetime.now() + timedelta(days=7, hours=4),
            "expected_participants": 50,
            "location_text": "Городской парк Подольска",
            "status": EventStatus.APPROVED,
            "created_by_id": citizen.id,
            "responsible_user_id": admin.id
        },
        {
            "title": "Ярмарка выходного дня",
            "event_type": "fair",
            "description": "Ярмарка местных производителей.",
            "start_date": datetime.now() + timedelta(days=14),
            "end_date": datetime.now() + timedelta(days=14, hours=8),
            "expected_participants": 200,
            "location_text": "Центральная площадь",
            "status": EventStatus.PENDING_APPROVAL,
            "created_by_id": citizen.id
        },
        {
            "title": "Концерт на открытом воздухе",
            "event_type": "concert",
            "description": "Музыкальный вечер с местными артистами.",
            "start_date": datetime.now() + timedelta(days=21),
            "expected_participants": 100,
            "location_text": "Набережная реки Пахры",
            "status": EventStatus.DRAFT,
            "created_by_id": citizen.id
        }
    ]

    for data in events_data:
        event = EventRequest(**data)
        db.add(event)

    db.commit()
    print("Events seeded.")