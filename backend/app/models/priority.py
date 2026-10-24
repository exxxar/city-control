# priority.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class Priority(TimestampMixin, Base):
    __tablename__ = "priorities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column(Integer, unique=True) # 1=critical, 2=high, etc.
    color: Mapped[str] = mapped_column(String(20), default="#FF0000")