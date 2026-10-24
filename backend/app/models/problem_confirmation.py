# problem_confirmation.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class ProblemConfirmation(TimestampMixin, Base):
    __tablename__ = "problem_confirmations"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_verified: Mapped[bool] = mapped_column(default=False) # e.g., via GPS/QR