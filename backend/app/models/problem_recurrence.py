# problem_recurrence.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class ProblemRecurrence(TimestampMixin, Base):
    __tablename__ = "problem_recurrences"
    id: Mapped[int] = mapped_column(primary_key=True)
    original_problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    new_problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))