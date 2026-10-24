from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class ResponsibilityTransfer(TimestampMixin, Base):
    __tablename__ = "responsibility_transfers"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    from_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    from_org_id: Mapped[int | None] = mapped_column(ForeignKey("executor_organizations.id"))
    to_org_id: Mapped[int | None] = mapped_column(ForeignKey("executor_organizations.id"))

    reason: Mapped[str | None] = mapped_column(String(255))
    comment: Mapped[str | None] = mapped_column(Text)
    transferred_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))