# offline_sync_record.py
import enum
from sqlalchemy import String, Integer, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class SyncStatus(str, enum.Enum):
    PENDING = "pending"
    SYNCED = "synced"
    FAILED = "failed"


class OfflineSyncRecord(TimestampMixin, Base):
    __tablename__ = "offline_sync_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    entity_type: Mapped[str] = mapped_column(String(50))  # problem, initiative
    action: Mapped[str] = mapped_column(String(20))  # create, update
    payload: Mapped[dict] = mapped_column(JSON)

    status: Mapped[SyncStatus] = mapped_column(SQLEnum(SyncStatus), default=SyncStatus.PENDING)
    sync_error: Mapped[str | None] = mapped_column(String(500))