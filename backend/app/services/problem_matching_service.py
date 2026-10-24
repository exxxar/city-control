from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.problem import Problem
from app.repositories.problem_repository import ProblemRepository


class ProblemMatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProblemRepository(db)

    def find_similar(
            self,
            category_id: Optional[int],
            territory_id: Optional[int],
            latitude: Optional[float],
            longitude: Optional[float],
            radius_m: float = 100.0
    ) -> List[Problem]:
        """
        Ищет похожие открытые проблемы по категории и локации.
        В продакшене здесь должен быть сложный запрос с PostGIS/MySQL Spatial
        или формулой Хаверсина для точного расчета расстояния.
        """
        if not category_id:
            return []

        return self.repo.find_similar_problems(
            latitude=latitude or 0.0,
            longitude=longitude or 0.0,
            category_id=category_id,
            radius_km=radius_m / 1000
        )