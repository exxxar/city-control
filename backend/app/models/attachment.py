# attachment.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class Attachment(TimestampMixin, Base):
    __tablename__ = "attachments"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_url: Mapped[str] = mapped_column(String(500))
    file_name: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100))
    file_size: Mapped[int] = mapped_column(Integer)  # in bytes

    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Полиморфная связь (с чем связан файл: проблема, инициатива, чат и т.д.)
    linked_entity_type: Mapped[str] = mapped_column(String(50))
    linked_entity_id: Mapped[int] = mapped_column(Integer)