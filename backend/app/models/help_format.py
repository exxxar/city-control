from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from app.db.base import Base  # Убедитесь, что путь к Base верный!

class HelpFormat(Base):
    __tablename__ = "help_formats"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)