from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.territory import Territory, TerritoryLevel

TERRITORIES_DATA = [
    {
        "name": "Россия", "code": "RU", "level": TerritoryLevel.COUNTRY,
        "children": [
            {
                "name": "Московская область", "code": "MO", "level": TerritoryLevel.REGION,
                "children": [
                    {
                        "name": "Городской округ Подольск", "code": "PODOLSK", "level": TerritoryLevel.MUNICIPALITY,
                        "children": [
                            {"name": "Улица Ленина", "code": "LENINA_ST", "level": TerritoryLevel.STREET},
                            {"name": "Улица Кирова", "code": "KIROVA_ST", "level": TerritoryLevel.STREET},
                        ]
                    }
                ]
            }
        ]
    }
]


def _create_territories_recursive(db: Session, data_list: list, parent_id: int | None = None):
    for data in data_list:
        stmt = select(Territory).where(Territory.code == data["code"])
        territory = db.execute(stmt).scalar_one_or_none()

        if not territory:
            territory = Territory(
                name=data["name"],
                code=data["code"],
                level=data["level"],
                parent_id=parent_id
            )
            db.add(territory)
            db.flush()  # Получаем territory.id

        children = data.get("children", [])
        if children:
            _create_territories_recursive(db, children, territory.id)


def seed_territories(db: Session):
    print("Seeding territories...")
    _create_territories_recursive(db, TERRITORIES_DATA)
    db.commit()
    print("Territories seeded.")