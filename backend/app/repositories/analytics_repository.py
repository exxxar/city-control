# backend/app/repositories/analytics_repository.py
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.problem import Problem, ProblemStatus
from app.models.territory import Territory


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_kpi(self) -> Dict[str, Any]:
        total = self.db.execute(select(func.count(Problem.id))).scalar() or 0
        new_today = self.db.execute(
            select(func.count(Problem.id)).where(
                Problem.status == ProblemStatus.NEW,
                Problem.created_at >= datetime.utcnow() - timedelta(days=1)
            )
        ).scalar() or 0

        in_progress = self.db.execute(
            select(func.count(Problem.id)).where(Problem.status == ProblemStatus.IN_PROGRESS)
        ).scalar() or 0

        resolved = self.db.execute(
            select(func.count(Problem.id)).where(Problem.status == ProblemStatus.RESOLVED)
        ).scalar() or 0

        return {
            "total_problems": total,
            "new_problems_today": new_today,
            "in_progress": in_progress,
            "resolved_total": resolved
        }

    def get_heatmap_data(self, territory_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Возвращает список точек для тепловой карты.
        Упрощенно: берем координаты из связанных GeoTag.
        """
        # Для прототипа возвращаем мок-данные
        return [
            {"latitude": 55.1, "longitude": 37.1, "weight": 10},
            {"latitude": 55.2, "longitude": 37.2, "weight": 5},
            {"latitude": 55.15, "longitude": 37.15, "weight": 15}
        ]

    def get_territory_index(self, territory_id: int) -> Dict[str, Any]:
        """
        Расчет индекса состояния территории (0-100).
        """
        territory = self.db.get(Territory, territory_id)
        if not territory:
            return {}

        # Упрощенная логика расчета
        problems_count = self.db.execute(
            select(func.count(Problem.id)).where(Problem.territory_id == territory_id)
        ).scalar() or 0

        active_problems = self.db.execute(
            select(func.count(Problem.id)).where(
                Problem.territory_id == territory_id,
                Problem.status.notin_([ProblemStatus.RESOLVED, ProblemStatus.CLOSED])
            )
        ).scalar() or 0

        # Индекс = 100 - (active_problems * 2)
        index_score = max(0, 100 - (active_problems * 2))

        return {
            "territory_id": territory_id,
            "territory_name": territory.name,
            "index_score": index_score,
            "total_problems": problems_count,
            "active_problems": active_problems
        }