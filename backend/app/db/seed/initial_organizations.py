from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.executor_organization import ExecutorOrganization
from app.models.territory import Territory

ORGS_DATA = [
    {"name": "Департамент благоустройства и ЖКХ", "email": "zhkh@city.local", "territory_code": "PODOLSK"},
    {"name": "Управление дорожным хозяйством", "email": "roads@city.local", "territory_code": "PODOLSK"},
    {"name": "Комитет по экологии", "email": "eco@city.local", "territory_code": "MO"},
]


def seed_organizations(db: Session):
    print("Seeding organizations...")
    for data in ORGS_DATA:
        stmt = select(ExecutorOrganization).where(ExecutorOrganization.name == data["name"])
        if not db.execute(stmt).scalar_one_or_none():
            # Привязываем к территории, если нашли её
            terr_stmt = select(Territory).where(Territory.code == data["territory_code"])
            territory = db.execute(terr_stmt).scalar_one_or_none()

            db.add(ExecutorOrganization(
                name=data["name"],
                email=data["email"],
                territory_id=territory.id if territory else None
            ))
    db.commit()
    print("Organizations seeded.")