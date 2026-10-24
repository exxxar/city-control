# backend/app/models/report.py
import enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION = "revision"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    executor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    work_description: Mapped[str | None] = mapped_column(Text)
    work_date: Mapped[datetime | None] = mapped_column(DateTime)

    photos_before_count: Mapped[int] = mapped_column(Integer, default=0)
    photos_after_count: Mapped[int] = mapped_column(Integer, default=0)

    materials_used: Mapped[str | None] = mapped_column(Text)
    cost: Mapped[float] = mapped_column(Float, default=0.0)

    # 👇 ИСПРАВЛЕНИЕ ЗДЕСЬ: явно указываем использовать значения (values), а не имена (names)
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus, values_callable=lambda x: [e.value for e in x]),
        default=ReportStatus.PENDING
    )

    reject_reason: Mapped[str | None] = mapped_column(Text)
    revision_comment: Mapped[str | None] = mapped_column(Text)

    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    problem = relationship("Problem")
    executor = relationship("User", foreign_keys=[executor_id])