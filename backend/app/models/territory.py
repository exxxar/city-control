import enum
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

class TerritoryLevel(str, enum.Enum):
    COUNTRY = "country"; REGION = "region"; MUNICIPALITY = "municipality"
    DISTRICT = "district"; AREA = "area"; CITY = "city"; STREET = "street"

class Territory(TimestampMixin, Base):
    __tablename__ = "territories"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("territories.id"))
    name: Mapped[str] = mapped_column(String(255))
    level: Mapped[TerritoryLevel] = mapped_column(SQLEnum(TerritoryLevel))
    code: Mapped[str | None] = mapped_column(String(50), index=True)
    parent: Mapped["Territory"] = relationship("Territory", remote_side=[id], lazy="selectin")