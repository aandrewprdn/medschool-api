from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from src.orm.models.base import BaseOrmModel
from src.orm.models.client import ClientOrmModel


class LessonOrmModel(BaseOrmModel):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    state: Mapped[str] = mapped_column(
        String, default="OPEN_FOR_BOOKING", nullable=False
    )

    clients: Mapped[list[ClientOrmModel]] = relationship(
        secondary="lessons_clients", back_populates="lessons"
    )
