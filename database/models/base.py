from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# pylint: disable=all
class BaseModel(DeclarativeBase, MappedAsDataclass): ...
