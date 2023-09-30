from typing import TYPE_CHECKING, List
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db import Base

if TYPE_CHECKING:
    from src.users.models import User


class BookingType(Base):
    __tablename__ = "booking_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    def __str__(self) -> str:
        return f"{__class__.__name__} {self.name!r}"

    def __repr__(self) -> str:
        return str(self)


class Bookings(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    booking_type: Mapped[int] = mapped_column(ForeignKey("booking_type.id"))
    booking_date: Mapped[datetime.date]
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="bookings")

    def __str__(self) -> str:
        return f"{__class__.__name__} {self.id!r}"

    def __repr__(self) -> str:
        return str(self)
