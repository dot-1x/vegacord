from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import guild_only, option, slash_command
from bot.exceptions import MemberAlreadyChangedError
from bot.extensions.abcextension import ABCExtension
from bot.utils.dbutils import get_member_data, update_member
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
        try:
            await update_member(ctx.author.id, ign=ign, server=server)
        except MemberAlreadyChangedError:
            return await ctx.respond("You've already changed your data before")
        embed = build_embed(
            title=f"{ctx.author.name} in-game data recorded as:",
            message=f"> Nickname: {ign}\n> Server: {server}",
        )
        await ctx.respond(
            "succesfully update your in-game data with", embed=embed, ephemeral=True
        )

    @guild_only()
    @slash_command(name="get-data", description="Get in-game data of a user")
    @option(
        name="user",
        type=discord.Member,
        description="Target member",
        required=False,
        default=None,
    )
    async def get_igdata(
        self, ctx: discord.ApplicationContext, user: discord.Member | None = None
    ):
        target = user or ctx.author
        found = await get_member_data(target.id)
        if not found:
            return await ctx.respond(
                embed=build_embed(
                    message=f"cannot find in-game data for user {target.mention}"
                )
            )
        embed = build_embed(
            title=f"{target.name} in-game data recorded as:",
            message=f"> Nickname: {found.ingame}\n> Server: {found.server}",
        )
        return await ctx.respond(embed=embed)
