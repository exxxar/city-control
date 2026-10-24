# document.py
import enum
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class DocumentType(str, enum.Enum):
    PROBLEM_CARD = "problem_card"  # Автогенерируемый DOCX
    ACT = "act"
    REPORT = "report"


class Document(TimestampMixin, Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    doc_type: Mapped[DocumentType] = mapped_column(SQLEnum(DocumentType))
    file_url: Mapped[str] = mapped_column(String(500))
    file_name: Mapped[str] = mapped_column(String(255))

    problem_id: Mapped[int | None] = mapped_column(ForeignKey("problems.id"))
    generated_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))