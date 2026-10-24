from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.sla_policy import SlaPolicy
from app.models.priority import Priority

SLA_DATA = [
    {"priority_level": 1, "reaction_mins": 30, "resolution_mins": 240},  # Критический: 30 мин / 4 часа
    {"priority_level": 2, "reaction_mins": 120, "resolution_mins": 1440},  # Высокий: 2 часа / 24 часа
    {"priority_level": 3, "reaction_mins": 720, "resolution_mins": 4320},  # Средний: 12 часов / 3 суток
    {"priority_level": 4, "reaction_mins": 1440, "resolution_mins": 10080},  # Низкий: 24 часа / 7 суток
]


def seed_sla(db: Session):
    print("Seeding SLA policies...")

    priorities_stmt = select(Priority)
    priorities_map = {p.level: p for p in db.execute(priorities_stmt).scalars().all()}

    for data in SLA_DATA:
        priority = priorities_map.get(data["priority_level"])
        if not priority:
            continue

        stmt = select(SlaPolicy).where(SlaPolicy.priority_id == priority.id)
        if not db.execute(stmt).scalar_one_or_none():
            db.add(SlaPolicy(
                name=f"SLA для приоритета '{priority.name}'",
                priority_id=priority.id,
                reaction_time_minutes=data["reaction_mins"],
                resolution_time_minutes=data["resolution_mins"]
            ))

    db.commit()
    print("SLA policies seeded.")