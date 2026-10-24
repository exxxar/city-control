from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserReadShort


class ProblemMessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)


class ProblemMessageRead(BaseModel):
    id: int
    problem_id: int
    user_id: Optional[int] = None
    content: str
    is_system: bool
    created_at: datetime

    user: Optional[UserReadShort] = None

    model_config = ConfigDict(from_attributes=True)