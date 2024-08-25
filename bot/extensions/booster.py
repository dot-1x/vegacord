from __future__ import annotations
from typing import TYPE_CHECKING, Any

import discord
from bot.extensions.abcextension import ABCExtension

if TYPE_CHECKING:
    from bot.bot import BaseBot


class BoosterExt(discord.Cog, ABCExtension):
    ENABLED = True

    def __init__(self, bot: BaseBot) -> None:
        self.bot = bot
