from __future__ import annotations
from itertools import islice
from typing import TYPE_CHECKING, Any

import discord
from discord import guild_only, slash_command
from bot.extensions.abcextension import ABCExtension
from bot.utils.decorators import is_admin
from bot.utils.generators import chunk_list

if TYPE_CHECKING:
    from bot.bot import BaseBot


class BoosterExt(discord.Cog, ABCExtension):
    ENABLED = True

    def __init__(self, bot: BaseBot) -> None:
        self.bot = bot

    @discord.Cog.listener()
    async def on_member_update(self, _: discord.Member, after: discord.Member):
        if after.get_role(self.bot.master_guild.premium_subscriber_role):
            ...

    @is_admin()
    @guild_only()
    @slash_command(
        name="boosters",
        description="Command to check server booster list and valid registered booster reward",
    )
    async def check_booster(self, ctx: discord.ApplicationContext):
        boosters = ctx.interaction.guild.premium_subscribers
        booster_text = "\n".join(
            "    ".join(member.mention for member in booster)
            for booster in chunk_list(boosters)
        )
        embed = discord.Embed(color=discord.Colour.nitro_pink())
        embed.description = booster_text

        return await ctx.respond(
            f"_Currently **{len(boosters)}** members is boosting this server_",
            ephemeral=True,
            embed=embed,
        )
