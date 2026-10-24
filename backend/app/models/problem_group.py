# problem_group.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class ProblemGroup(TimestampMixin, Base):
    __tablename__ = "problem_groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    total_problems: Mapped[int] = mapped_column(Integer, default=0)