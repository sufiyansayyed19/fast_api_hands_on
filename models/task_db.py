from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base


class TaskDB(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]

    description: Mapped[str | None]

    completed: Mapped[bool] = mapped_column(
        default=False
    )

    priority: Mapped[str] = mapped_column(
        default="medium"
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')"
        ),

        UniqueConstraint(
            "user_id",
            "title"
        ),
    )