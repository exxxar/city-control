from typing import List, Optional
from pydantic import BaseModel

class DashboardKPI(BaseModel):
    total_problems: int
    new_problems_today: int
    in_progress: int
    overdue_sla: int
    resolved_today: int
    avg_resolution_hours: float

class HeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    weight: int # Интенсивность (количество проблем или критичность)

class HeatmapResponse(BaseModel):
    points: List[HeatmapPoint]

class TerritoryIndex(BaseModel):
    territory_id: int
    territory_name: str
    index_score: float # 0-100
    active_problems: int
    avg_resolution_time_hours: float
    overdue_percentage: float