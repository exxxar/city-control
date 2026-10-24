# before_after_media.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class BeforeAfterMedia(TimestampMixin, Base):
    __tablename__ = "before_after_media"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    before_attachment_id: Mapped[int] = mapped_column(ForeignKey("attachments.id"))
    after_attachment_id: Mapped[int] = mapped_column(ForeignKey("attachments.id"))
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))