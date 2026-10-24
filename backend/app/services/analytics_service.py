from sqlalchemy.orm import Session
from app.repositories.analytics_repository import AnalyticsRepository

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AnalyticsRepository(db)

    def get_dashboard_data(self):
        return self.repo.get_dashboard_kpi()

    def get_heatmap_points(self, territory_id: int = None):
        return self.repo.get_heatmap_data(territory_id)

    def calculate_territory_index(self, territory_id: int):
        return self.repo.get_territory_index(territory_id)