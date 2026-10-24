# backend/app/repositories/territory_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.territory import Territory, TerritoryLevel

class TerritoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, territory_id: int) -> Optional[Territory]:
        return self.db.get(Territory, territory_id)

    def get_by_code(self, code: str) -> Optional[Territory]:
        stmt = select(Territory).where(Territory.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> List[Territory]:
        stmt = select(Territory)
        return list(self.db.execute(stmt).scalars().all())

    def get_children(self, parent_id: int) -> List[Territory]:
        stmt = select(Territory).where(Territory.parent_id == parent_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_roots(self) -> List[Territory]:
        stmt = select(Territory).where(Territory.parent_id == None)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, territory: Territory) -> Territory:
        self.db.add(territory)
        self.db.commit()
        self.db.refresh(territory)
        return territory