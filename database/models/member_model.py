from datetime import datetime
from database.models.base import BaseModel
from sqlalchemy import BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Booster(BaseModel):
    __tablename__ = "booster"

    userid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    boosting_since: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    expired_since: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    isboosting: Mapped[bool] = mapped_column(default=False)

    @property
    def boosting(self):
        return (
            f"<t:{self.boosting_since.timestamp():.0f}>"
            if self.boosting_since
            else None
        )

    @property
    def expired(self):
        return (
            f"<t:{self.expired_since.timestamp():.0f}>" if self.expired_since else None
        )


class Member(BaseModel):
    __tablename__ = "members"

    userid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ingame: Mapped[str] = mapped_column()
    server: Mapped[int] = mapped_column()
    has_changed: Mapped[bool] = mapped_column(default=False)
