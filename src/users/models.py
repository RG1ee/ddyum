from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    telegram: Mapped[str | None]
    phone: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=False)

    def __str__(self) -> str:
        return f"{__class__.__name__} {self.email!r}"

    def __repr__(self) -> str:
        return str(self)
