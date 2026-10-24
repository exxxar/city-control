# backend/app/db/seed/initial_problems.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.problem import Problem, ProblemStatus, ProblemType
from app.models.user import User
from app.models.category import Category
from app.models.priority import Priority
from app.models.geo_tag import GeoTag
from app.models.territory import Territory


def seed_problems(db: Session):
    print("Seeding problems...")

    if db.execute(select(Problem)).first():
        print("Problems already exist, skipping.")
        return

    # Получаем пользователей
    citizen = db.execute(select(User).where(User.email == "citizen@city.local")).scalar_one()
    admin = db.execute(select(User).where(User.email == "admin@city.local")).scalar_one()
    executor = db.execute(select(User).where(User.email == "executor@city.local")).scalar_one()

    # Получаем категории
    potholes = db.execute(select(Category).where(Category.slug == "road-potholes")).scalar_one()
    lighting = db.execute(select(Category).where(Category.slug == "street-lighting-outage")).scalar_one()
    garbage = db.execute(select(Category).where(Category.slug == "garbage-issues")).scalar_one()
    elevator = db.execute(select(Category).where(Category.slug == "broken-elevators")).scalar_one()

    # Получаем приоритеты
    critical = db.execute(select(Priority).where(Priority.level == 1)).scalar_one()
    high = db.execute(select(Priority).where(Priority.level == 2)).scalar_one()
    medium = db.execute(select(Priority).where(Priority.level == 3)).scalar_one()
    low = db.execute(select(Priority).where(Priority.level == 4)).scalar_one()

    # Получаем гео-метки
    geo_tags = db.execute(select(GeoTag)).scalars().all()

    # Получаем территорию
    podolsk = db.execute(select(Territory).where(Territory.code == "PODOLSK")).scalar_one()

    # Создаём проблемы
    problems_data = [
        {
            "title": "Огромная яма на дороге",
            "description": "На улице Ленина образовалась огромная яма, опасно для пешеходов и автомобилей.",
            "status": ProblemStatus.NEW,
            "type": ProblemType.PROBLEM,
            "category_id": potholes.id,
            "priority_id": high.id,
            "territory_id": podolsk.id,
            "geo_tag_id": geo_tags[0].id if geo_tags else None,
            "created_by_id": citizen.id,
            "assigned_to_id": executor.id,
            "rating": 5.0,
            "confirmations_count": 3
        },
        {
            "title": "Не работает уличное освещение",
            "description": "Темно вечером, опасно ходить.",
            "status": ProblemStatus.IN_PROGRESS,
            "type": ProblemType.PROBLEM,
            "category_id": lighting.id,
            "priority_id": medium.id,
            "territory_id": podolsk.id,
            "geo_tag_id": geo_tags[1].id if len(geo_tags) > 1 else None,
            "created_by_id": citizen.id,
            "assigned_to_id": executor.id,
            "rating": 3.5,
            "confirmations_count": 2
        },
        {
            "title": "Переполненный мусорный контейнер",
            "description": "Контейнер не вывозят уже неделю, запах ужасный.",
            "status": ProblemStatus.CONFIRMED,
            "type": ProblemType.PROBLEM,
            "category_id": garbage.id,
            "priority_id": high.id,
            "territory_id": podolsk.id,
            "geo_tag_id": geo_tags[2].id if len(geo_tags) > 2 else None,
            "created_by_id": citizen.id,
            "rating": 4.0,
            "confirmations_count": 5
        },
        {
            "title": "Сломанный лифт в подъезде",
            "description": "Лифт не работает уже 3 дня, пожилым людям тяжело подниматься.",
            "status": ProblemStatus.ACCEPTED,
            "type": ProblemType.PROBLEM,
            "category_id": elevator.id,
            "priority_id": critical.id,
            "territory_id": podolsk.id,
            "geo_tag_id": geo_tags[3].id if len(geo_tags) > 3 else None,
            "created_by_id": citizen.id,
            "assigned_to_id": executor.id,
            "rating": 8.0,
            "confirmations_count": 7
        },
        {
            "title": "Поваленное дерево на тротуаре",
            "description": "Дерево упало после storms, перекрывает проход.",
            "status": ProblemStatus.RESOLVED,
            "type": ProblemType.PROBLEM,
            "category_id": potholes.id,
            "priority_id": medium.id,
            "territory_id": podolsk.id,
            "created_by_id": citizen.id,
            "assigned_to_id": executor.id,
            "rating": 2.0,
            "confirmations_count": 1
        }
    ]

    for data in problems_data:
        problem = Problem(**data)
        db.add(problem)

    db.commit()
    print("Problems seeded.")