# initiative.py
import enum
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class InitiativeStatus(str, enum.Enum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Initiative(TimestampMixin, Base):
    __tablename__ = "initiatives"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[InitiativeStatus] = mapped_column(SQLEnum(InitiativeStatus), default=InitiativeStatus.NEW)

    territory_id: Mapped[int | None] = mapped_column(ForeignKey("territories.id"))
    geo_tag_id: Mapped[int | None] = mapped_column(ForeignKey("geo_tags.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    support_count: Mapped[int] = mapped_column(default=0)