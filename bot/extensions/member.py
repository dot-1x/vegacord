from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import guild_only, option, slash_command
from bot.extensions.abcextension import ABCExtension
from bot.utils.dbutils import update_member
from bot.utils.misc import build_embed

if TYPE_CHECKING:
    from bot.bot import BaseBot


class MemberExt(discord.Cog, ABCExtension):
    ENABLED = True

    def __init__(self, bot: BaseBot) -> None:
        super().__init__()

    @guild_only()
    @slash_command(
        name="update-data",
        description="Update your in-game data for giveaway or booster reward",
    )
    @option(name="ign", type=str, description="Your in-game nickname")
    @option(name="server", type=int, description="Your in-game server")
    async def fill_data(self, ctx: discord.ApplicationContext, ign: str, server: int):
        await ctx.defer(ephemeral=True)
        await update_member(ctx.author.id, ign=ign, server=server)
        embed = build_embed(
            title=f"{ctx.author.name} in-game data recorded as:",
            message=f"> Nickname: {ign}\n> Server: {server}",
        )
        await ctx.respond(
            "succesfully update your in-game data with", embed=embed, ephemeral=True
        )
