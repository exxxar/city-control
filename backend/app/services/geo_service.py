import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.geo_tag import GeoTag, GeoTagType
from app.repositories.geo_repository import GeoRepository
from app.services.notification_service import NotificationService


class GeoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = GeoRepository(db)
        self.notification_service = NotificationService(db)

    def create_gps_tag(self, lat: float, lng: float, radius_m: float = 50.0) -> GeoTag:
        tag = GeoTag(
            type=GeoTagType.GPS, latitude=lat, longitude=lng, radius=radius_m,
            notification_enabled=True, notification_radius=radius_m, active=True
        )
        return self.repo.create(tag)

    def create_qr_tag(self, building_id: Optional[int] = None, room_id: Optional[int] = None) -> GeoTag:
        tag = GeoTag(
            type=GeoTagType.QR, qr_token=str(uuid.uuid4()),
            building_id=building_id, room_id=room_id, active=True
        )
        return self.repo.create(tag)

    def process_user_location(self, user_id: int, lat: float, lng: float):
        """
        Проверяет попадание пользователя в зоны активных гео-меток и триггерит уведомления.
        Вызывается, когда фронтенд отправляет обновленные координаты пользователя.
        """
        nearby_tags = self.repo.find_nearby(lat, lng, radius_m=1000)
        active_tags = [t for t in nearby_tags if t.notification_enabled]

        if active_tags:
            # Группируем уведомления, чтобы не спамить (согласно концепту)
            self.notification_service.notify_geo_zone_entry(user_id, active_tags)

    def log_qr_scan(self, qr_token: str, user_id: int) -> GeoTag | None:
        tag = self.repo.get_by_qr_token(qr_token)
        if tag:
            self.repo.log_event(tag.id, user_id, "scan", metadata=f"QR scanned: {qr_token}")
        return tag