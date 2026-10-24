# sla_policy.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class SlaPolicy(TimestampMixin, Base):
    __tablename__ = "sla_policies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    # Можно привязать к категории или приоритету
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    priority_id: Mapped[int | None] = mapped_column(ForeignKey("priorities.id"))

    reaction_time_minutes: Mapped[int] = mapped_column(Integer)  # SLA на первичную реакцию
    resolution_time_minutes: Mapped[int] = mapped_column(Integer)  # SLA на устранение