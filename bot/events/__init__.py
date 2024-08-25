from typing import TYPE_CHECKING
from discord import Cog

from logs.log import get_logger


from .modmail import ModMail

if TYPE_CHECKING:
    from bot.bot import BaseBot

cogs: list[Cog] = [ModMail]
_log = get_logger("EVENTS")


def setup(bot: "BaseBot"):
    for cog in cogs:
        bot.add_cog(cog(bot))
        _log.info("Loaded event: %s", str(cog))
