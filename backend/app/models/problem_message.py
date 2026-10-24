# problem_message.py
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class ProblemMessage(TimestampMixin, Base):
    __tablename__ = "problem_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id")) # Null for system messages
    content: Mapped[str] = mapped_column(Text)
    is_system: Mapped[bool] = mapped_column(default=False)