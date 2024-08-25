from typing import TYPE_CHECKING
import discord

from bot.extensions.abcextension import ABCExtension
from logs.log import get_logger

if TYPE_CHECKING:
    from bot.bot import BaseBot

_log = get_logger("MODMAIL")


class ModMail(discord.Cog):
    def __init__(self, bot: "BaseBot") -> None:
        self.bot = bot

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        _log.info("Message passed")
        _log.info("Guild: %s", self.bot.get_guild(1219937222661509121))

    async def process_modmail(self, messaage: discord.Message):
        guild = await self.bot.master_guild()
        guild.categories
