import enum
from sqlalchemy import String, Integer, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class AssessmentFeedback(str, enum.Enum):
    FULLY_RESOLVED = "fully_resolved"
    PARTIALLY_RESOLVED = "partially_resolved"
    NOT_RESOLVED = "not_resolved"
    RECURRENCE = "recurrence"  # Возникла снова


class ResolutionAssessment(TimestampMixin, Base):
    __tablename__ = "resolution_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    rating: Mapped[int] = mapped_column(Integer)  # 1 to 5 stars
    feedback: Mapped[AssessmentFeedback] = mapped_column(SQLEnum(AssessmentFeedback))
    comment: Mapped[str | None] = mapped_column(Text)