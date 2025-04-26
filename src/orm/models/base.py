from sqlalchemy.orm import DeclarativeBase


class BaseOrmModel(DeclarativeBase):
    def __repr__(self) -> str:
        """Prettier print models for debug e.t.c , later can be removed"""

        columns = [
            f"{column}={getattr(self, column)}"
            for column in self.__table__.columns.keys()
        ]

        return f"<{self.__class__.__name__} {', '.join(columns)}>"
