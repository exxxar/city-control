# backend/app/repositories/geo_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.geo_tag import GeoTag, GeoTagType
from app.models.geo_tag_event import GeoTagEvent

class GeoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, geo_tag_id: int) -> Optional[GeoTag]:
        return self.db.get(GeoTag, geo_tag_id)

    def get_by_qr_token(self, qr_token: str) -> Optional[GeoTag]:
        stmt = select(GeoTag).where(GeoTag.qr_token == qr_token)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_active_geotags(self) -> List[GeoTag]:
        stmt = select(GeoTag).where(GeoTag.active == True)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, geo_tag: GeoTag) -> GeoTag:
        self.db.add(geo_tag)
        self.db.commit()
        self.db.refresh(geo_tag)
        return geo_tag

    def find_nearby(self, latitude: float, longitude: float, radius_m: float = 1000) -> List[GeoTag]:
        """
        Поиск ближайших активных гео-меток.
        Упрощенная логика для прототипа.
        """
        # В реальности здесь должен быть сложный запрос с формулой Хаверсина или Spatial Index
        all_tags = self.list_active_geotags()
        nearby = []
        for tag in all_tags:
            if tag.latitude and tag.longitude:
                # Очень грубая оценка расстояния (не для продакшена)
                dist = ((tag.latitude - latitude)**2 + (tag.longitude - longitude)**2)**0.5 * 111000
                if dist <= radius_m:
                    nearby.append(tag)
        return nearby

    def log_event(self, geo_tag_id: int, user_id: Optional[int], event_type: str, metadata: Optional[str] = None) -> GeoTagEvent:
        event = GeoTagEvent(
            geo_tag_id=geo_tag_id,
            user_id=user_id,
            event_type=event_type,
            metadata=metadata
        )
        self.db.add(event)
        self.db.commit()
        return event