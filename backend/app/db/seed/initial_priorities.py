from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.priority import Priority

PRIORITIES_DATA = [
    {"name": "Критический", "level": 1, "color": "#FF0000"}, # Красный (Аварии, угроза жизни)
    {"name": "Высокий", "level": 2, "color": "#FFA500"},     # Оранжевый (Серьезные нарушения)
    {"name": "Средний", "level": 3, "color": "#FFD700"},     # Желтый (Стандартные проблемы)
    {"name": "Низкий", "level": 4, "color": "#32CD32"},      # Зеленый (Косметические, улучшения)
]

def seed_priorities(db: Session):
    print("Seeding priorities...")
    for data in PRIORITIES_DATA:
        stmt = select(Priority).where(Priority.level == data["level"])
        if not db.execute(stmt).scalar_one_or_none():
            db.add(Priority(**data))
    db.commit()
    print("Priorities seeded.")