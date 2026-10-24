# initiative_support.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class InitiativeSupport(TimestampMixin, Base):
    __tablename__ = "initiative_supports"
    id: Mapped[int] = mapped_column(primary_key=True)
    initiative_id: Mapped[int] = mapped_column(ForeignKey("initiatives.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))