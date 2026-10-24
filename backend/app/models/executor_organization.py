# executor_organization.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class ExecutorOrganization(TimestampMixin, Base):
    __tablename__ = "executor_organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    territory_id: Mapped[int | None] = mapped_column(ForeignKey("territories.id"))
    email: Mapped[str | None] = mapped_column(String(255))