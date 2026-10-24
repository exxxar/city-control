from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.resolution_assessment import AssessmentFeedback

# --- SLA Policy ---
class SlaPolicyRead(BaseModel):
    id: int
    name: str
    category_id: Optional[int] = None
    priority_id: Optional[int] = None
    reaction_time_minutes: int
    resolution_time_minutes: int
    model_config = ConfigDict(from_attributes=True)

# --- SLA Timer ---
class SlaTimerRead(BaseModel):
    id: int
    problem_id: int
    reaction_deadline: datetime
    resolution_deadline: datetime
    is_reaction_met: bool
    is_resolution_met: bool
    model_config = ConfigDict(from_attributes=True)

# --- Responsibility Transfer ---
class ResponsibilityTransferCreate(BaseModel):
    to_user_id: int
    to_org_id: Optional[int] = None
    reason: Optional[str] = None
    comment: Optional[str] = None

class ResponsibilityTransferRead(BaseModel):
    id: int
    problem_id: int
    from_user_id: Optional[int] = None
    to_user_id: int
    reason: Optional[str] = None
    comment: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Resolution Assessment ---
class ResolutionAssessmentCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback: AssessmentFeedback
    comment: Optional[str] = None

class ResolutionAssessmentRead(BaseModel):
    id: int
    problem_id: int
    user_id: int
    rating: int
    feedback: AssessmentFeedback
    comment: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)