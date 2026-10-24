# sla_timer.py
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class SlaTimer(TimestampMixin, Base):
    __tablename__ = "sla_timers"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    sla_policy_id: Mapped[int] = mapped_column(ForeignKey("sla_policies.id"))

    reaction_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    resolution_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    is_reaction_met: Mapped[bool] = mapped_column(Boolean, default=False)
    is_resolution_met: Mapped[bool] = mapped_column(Boolean, default=False)