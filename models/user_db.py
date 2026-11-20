from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]