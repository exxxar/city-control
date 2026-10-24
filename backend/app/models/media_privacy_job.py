# media_privacy_job.py
import enum
from sqlalchemy import String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class PrivacyJobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class MediaPrivacyJob(TimestampMixin, Base):
    __tablename__ = "media_privacy_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    attachment_id: Mapped[int] = mapped_column(ForeignKey("attachments.id"))
    status: Mapped[PrivacyJobStatus] = mapped_column(SQLEnum(PrivacyJobStatus), default=PrivacyJobStatus.PENDING)

    blur_faces: Mapped[bool] = mapped_column(Boolean, default=True)
    blur_plates: Mapped[bool] = mapped_column(Boolean, default=True)

    processed_file_url: Mapped[str | None] = mapped_column(String(500))
    error_message: Mapped[str | None] = mapped_column(String(500))