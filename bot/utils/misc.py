from datetime import datetime

from discord import Embed, Color


def build_embed(title: str = "", message: str = ""):
    return Embed(
        title=title,
        description=message,
        color=Color.blurple(),
        timestamp=datetime.now(),
    )
