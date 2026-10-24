# executor.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class Executor(TimestampMixin, Base):
    __tablename__ = "executors"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("executor_organizations.id"))
    is_primary: Mapped[bool] = mapped_column(default=False)