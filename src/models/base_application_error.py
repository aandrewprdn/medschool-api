from src.models.base import BaseEntityModel


class BaseApplicationException(Exception, BaseEntityModel):
    message: str
    details: str
    status_code: int
    url: str
