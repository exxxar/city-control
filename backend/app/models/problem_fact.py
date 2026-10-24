# problem_fact.py
from sqlalchemy import String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class ProblemFact(TimestampMixin, Base):
    __tablename__ = "problem_facts"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int | None] = mapped_column(ForeignKey("problems.id")) # Null if not grouped yet
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str | None] = mapped_column(Text)
    geo_data: Mapped[dict | None] = mapped_column(JSON)
    is_grouped: Mapped[bool] = mapped_column(default=False)