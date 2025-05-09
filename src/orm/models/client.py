from sqlalchemy import String, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.orm.models.base import BaseOrmModel
from src.orm.models.lesson import LessonOrmModel


class ClientOrmModel(BaseOrmModel):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    telegram_nickname: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=True)
    phone_number: Mapped[String] = mapped_column(JSON, nullable=True)
    status: Mapped[String] = mapped_column(String, default="ACTIVE")

    lessons: Mapped[list[LessonOrmModel]] = relationship(  # type: ignore[name-defined]
        secondary="lessons_clients",
        back_populates="clients",
    )
