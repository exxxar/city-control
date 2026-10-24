from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
from app.models.problem import ProblemStatus

class ProblemStatusHistory(TimestampMixin, Base):
    __tablename__ = "problem_status_histories"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    old_status: Mapped[ProblemStatus | None] = mapped_column(SQLEnum(ProblemStatus))
    new_status: Mapped[ProblemStatus] = mapped_column(SQLEnum(ProblemStatus))
    changed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment: Mapped[str | None] = mapped_column(Text)