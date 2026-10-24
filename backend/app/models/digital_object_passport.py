# digital_object_passport.py
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class DigitalObjectPassport(TimestampMixin, Base):
    __tablename__ = "digital_object_passports"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Привязка к зданию или муниципальному объекту
    building_id: Mapped[int | None] = mapped_column(ForeignKey("buildings.id"))
    municipal_object_id: Mapped[int | None] = mapped_column(ForeignKey("municipal_objects.id"))

    qr_token: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    summary_data: Mapped[dict | None] = mapped_column(JSON)  # Кэш основных данных для быстрого доступа по QR