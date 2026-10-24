from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.category import Category

# Иерархия категорий (Родитель -> Дети)
CATEGORIES_DATA = [
    {
        "name": "Дороги и транспорт",
        "slug": "roads-transport",
        "children": [
            {"name": "Ямы и выбоины на дорогах", "slug": "road-potholes"},
            {"name": "Неисправные светофоры", "slug": "broken-traffic-lights"},
            {"name": "Отсутствие разметки", "slug": "missing-road-markings"},
            {"name": "Проблемы с остановками", "slug": "bus-stops-issues"},
        ]
    },
    {
        "name": "ЖКХ и коммуникации",
        "slug": "utilities",
        "children": [
            {"name": "Прорывы труб / Затопления", "slug": "pipe-bursts"},
            {"name": "Не работает освещение", "slug": "street-lighting-outage"},
            {"name": "Мусор / Переполненные контейнеры", "slug": "garbage-issues"},
            {"name": "Проблемы с отоплением", "slug": "heating-issues"},
        ]
    },
    {
        "name": "Благоустройство и экология",
        "slug": "environment",
        "children": [
            {"name": "Сломанные лавочки / Урны", "slug": "broken-benches"},
            {"name": "Незаконные свалки", "slug": "illegal-dumps"},
            {"name": "Поваленные деревья / Ветки", "slug": "fallen-trees"},
            {"name": "Проблемы с детскими площадками", "slug": "playground-issues"},
        ]
    },
    {
        "name": "Здания и сооружения",
        "slug": "buildings",
        "children": [
            {"name": "Разрушающиеся фасады", "slug": "damaged-facades"},
            {"name": "Проблемы с крышами", "slug": "roof-issues"},
            {"name": "Неисправные лифты", "slug": "broken-elevators"},
            {"name": "Аварийное состояние", "slug": "emergency-condition"},
        ]
    },
]


def seed_categories(db: Session):
    print("Seeding categories...")

    for parent_data in CATEGORIES_DATA:
        # Проверяем родителя
        stmt = select(Category).where(Category.slug == parent_data["slug"])
        parent = db.execute(stmt).scalar_one_or_none()

        if not parent:
            parent = Category(
                name=parent_data["name"],
                slug=parent_data["slug"],
                parent_id=None
            )
            db.add(parent)
            db.flush()  # Чтобы получить parent.id

        # Добавляем детей
        for child_data in parent_data.get("children", []):
            stmt_child = select(Category).where(Category.slug == child_data["slug"])
            child = db.execute(stmt_child).scalar_one_or_none()

            if not child:
                child = Category(
                    name=child_data["name"],
                    slug=child_data["slug"],
                    parent_id=parent.id
                )
                db.add(child)

    db.commit()
    print("Categories seeded successfully.")