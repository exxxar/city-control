# backend/app/db/seed/initial_geo_tags.py
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.geo_tag import GeoTag, GeoTagType
from app.models.building import Building
from app.models.floor import Floor
from app.models.room import Room


def seed_geo_tags(db: Session):
    print("Seeding geo tags...")

    # Проверяем, есть ли уже гео-метки
    if db.execute(select(GeoTag)).first():
        print("Geo tags already exist, skipping.")
        return

    # Получаем территории для привязки
    from app.models.territory import Territory
    podolsk = db.execute(select(Territory).where(Territory.code == "PODOLSK")).scalar_one_or_none()
    lenina_st = db.execute(select(Territory).where(Territory.code == "LENINA_ST")).scalar_one_or_none()

    # 1. GPS-метки (уличные проблемы)
    gps_tags = [
        {"type": GeoTagType.GPS, "latitude": 55.4308, "longitude": 37.5450, "radius": 50.0,
         "notification_enabled": True, "notification_radius": 100.0, "active": True},
        {"type": GeoTagType.GPS, "latitude": 55.4315, "longitude": 37.5465, "radius": 30.0,
         "notification_enabled": True, "notification_radius": 80.0, "active": True},
        {"type": GeoTagType.GPS, "latitude": 55.4320, "longitude": 37.5470, "radius": 40.0,
         "notification_enabled": False, "active": True},
        {"type": GeoTagType.GPS, "latitude": 55.4305, "longitude": 37.5440, "radius": 60.0,
         "notification_enabled": True, "notification_radius": 120.0, "active": True},
    ]

    for data in gps_tags:
        tag = GeoTag(**data)
        db.add(tag)

    # 2. QR-метки (для зданий/помещений)
    qr_tags = [
        {"type": GeoTagType.QR, "qr_token": str(uuid.uuid4()), "notification_enabled": True, "active": True},
        {"type": GeoTagType.QR, "qr_token": str(uuid.uuid4()), "notification_enabled": True, "active": True},
        {"type": GeoTagType.QR, "qr_token": str(uuid.uuid4()), "notification_enabled": False, "active": True},
    ]

    for data in qr_tags:
        tag = GeoTag(**data)
        db.add(tag)

    # 3. Полигоны (зоны)
    polygon_tags = [
        {
            "type": GeoTagType.POLYGON,
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[37.544, 55.430], [37.546, 55.430], [37.546, 55.432], [37.544, 55.432], [37.544, 55.430]]]
            },
            "notification_enabled": True,
            "notification_radius": 200.0,
            "active": True
        },
        {
            "type": GeoTagType.POLYGON,
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[37.547, 55.431], [37.549, 55.431], [37.549, 55.433], [37.547, 55.433], [37.547, 55.431]]]
            },
            "notification_enabled": True,
            "active": True
        }
    ]

    for data in polygon_tags:
        tag = GeoTag(**data)
        db.add(tag)

    # 4. Indoor-метки (внутренние, привязаны к зданиям)
    # Сначала создадим тестовое здание, этаж и помещение
    building = Building(address="ул. Ленина, д. 10", name="Администрация Подольска",
                        territory_id=lenina_st.id if lenina_st else None)
    db.add(building)
    db.flush()

    floor = Floor(building_id=building.id, level=1, name="Первый этаж")
    db.add(floor)
    db.flush()

    room = Room(floor_id=floor.id, name="Каб. 101", room_type="office")
    db.add(room)
    db.flush()

    indoor_tag = GeoTag(
        type=GeoTagType.INDOOR,
        building_id=building.id,
        floor_id=floor.id,
        room_id=room.id,
        notification_enabled=True,
        active=True
    )
    db.add(indoor_tag)

    db.commit()
    print("Geo tags seeded.")