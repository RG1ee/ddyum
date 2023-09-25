from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["Profile"] = relationship(
        uselist=False,
        backref="profile",
    )

    def __str__(self) -> str:
        return f"{__class__.__name__} {self.email!r}"

    def __repr__(self) -> str:
        return str(self)


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    telegram: Mapped[str | None]
    phone: Mapped[str | None]

    user_profile: Mapped["User"] = relationship(backref="user")

    def __str__(self) -> str:
        return f"{__class__.__name__} {self.telegram!r}"

    def __repr__(self) -> str:
        return str(self)
