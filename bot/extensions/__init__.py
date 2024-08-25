from typing import TYPE_CHECKING
from discord import Cog

from logs.log import get_logger


from .booster import BoosterExt

if TYPE_CHECKING:
    from bot.extensions.abcextension import ABCExtension
    from bot.bot import BaseBot

cogs: list["ABCExtension"] = [BoosterExt]
_log = get_logger("EVENTS")


def setup(bot: "BaseBot"):
    for cog in cogs:
        if not cog.ENABLED:
            continue
        bot.add_cog(cog(bot))
        _log.info("Loaded event: %s", str(cog))
