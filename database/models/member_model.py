from datetime import datetime
from database.models.base import BaseModel
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Booster(BaseModel):
    __tablename__ = "booster"

    userid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    boosting_since: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    expired_since: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    isboosting: Mapped[bool] = mapped_column(default=False)


class Member(BaseModel):
    __tablename__ = "members"

    userid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ingame: Mapped[str] = mapped_column()
    server: Mapped[int] = mapped_column()
