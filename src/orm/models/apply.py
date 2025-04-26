import datetime
from typing import Literal, Type

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.orm.models.base import BaseOrmModel
from src.orm.models.client import ClientOrmModel
from src.orm.models.lesson import LessonOrmModel

ApplyState: Type[str] = Literal["CREATED", "ACCEPTED", "CANCELED", "FULLY_PAID"]


class ApplyOrmModel(BaseOrmModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sum: Mapped[int] = mapped_column(Integer, null=False)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, onupdate=lambda: datetime.datetime.now(datetime.UTC)
    )
    state: Mapped[ApplyState] = mapped_column(
        String(20), nullable=False, default="CREATED"
    )

    client: Mapped[ClientOrmModel] = relationship()
    lesson: Mapped[LessonOrmModel] = relationship()
