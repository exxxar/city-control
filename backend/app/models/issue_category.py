from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped
from app.db.base import Base  # Убедитесь, что путь к Base верный!

class IssueCategory(Base):
    __tablename__ = "issue_categories"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    icon: Mapped[Optional[str]] = Column(String(255), nullable=True)
    type: Mapped[int] = Column(Integer, nullable=False, default=0)  # 0=problem, 1=solution, 2=difficulty
    variants: Mapped[Optional[str]] = Column(Text, nullable=True)  # JSON-строка