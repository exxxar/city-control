# backend/app/models/problem.py
import enum
import uuid
from typing import Optional
from sqlalchemy import String, Integer, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class ProblemType(str, enum.Enum):
    PROBLEM = "problem"
    INITIATIVE = "initiative"
    EVENT = "event"


class ProblemStatus(str, enum.Enum):
    NEW = "new"
    NEEDS_CLARIFICATION = "needs_clarification"
    CONFIRMED = "confirmed"
    TRANSFERRED = "transferred"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    SUSPENDED = "suspended"
    SOLUTION_READY = "solution_ready"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


class Problem(TimestampMixin, Base):
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))

    type: Mapped[ProblemType] = mapped_column(SQLEnum(ProblemType), nullable=False, default=ProblemType.PROBLEM)
    status: Mapped[ProblemStatus] = mapped_column(SQLEnum(ProblemStatus), default=ProblemStatus.NEW, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    territory_id: Mapped[Optional[int]] = mapped_column(ForeignKey("territories.id", ondelete="SET NULL"))
    geo_tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("geo_tags.id", ondelete="SET NULL"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    priority_id: Mapped[Optional[int]] = mapped_column(ForeignKey("priorities.id", ondelete="SET NULL"))

    rating: Mapped[float] = mapped_column(Float, default=0.0)
    confirmations_count: Mapped[int] = mapped_column(Integer, default=0)

    # ИСПРАВЛЕНО: добавлено Optional[int]
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    assigned_to_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("problem_groups.id", ondelete="SET NULL"))

    created_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by_id], lazy="selectin")
    assigned_to: Mapped[Optional["User"]] = relationship("User", foreign_keys=[assigned_to_id], lazy="selectin")