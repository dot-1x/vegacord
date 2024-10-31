from datetime import datetime, timedelta, timezone

from discord import Embed, Color


def build_embed(title: str = "", message: str = ""):
    return Embed(
        title=title,
        description=message,
        color=Color.blurple(),
        timestamp=datetime.now(),
    )


def convert_jakarta(dt: datetime | None = None):
    if dt is None:
        return datetime.now(tz=timezone(timedelta(hours=7))).replace(tzinfo=None)
    return dt.astimezone(timezone(timedelta(hours=7))).replace(tzinfo=None)
