from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from src.orm.models.base import BaseOrmModel
from src.orm.models.clients import ClientsOrmModel


class LessonsOrmModel(BaseOrmModel):
    __tablename__ = "lessons"

    name: str = mapped_column(String, null=False)
    datetime: datetime = mapped_column(DateTime, null=False)
    price: int = mapped_column(Integer, null=False)
    state: str = mapped_column(String, default="OPEN_FOR_BOOKING", null=False)

    clients: Mapped[list[ClientsOrmModel]] = relationship(
        secondary="lessons_clients",
        back_populates="lessons"
    )