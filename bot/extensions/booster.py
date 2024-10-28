from __future__ import annotations
from typing import TYPE_CHECKING

import discord
from discord import guild_only, slash_command

from bot.extensions.abcextension import ABCExtension
from bot.logs.custom_logger import BotLogger
from bot.utils.generators import chunk_list
from bot.utils.misc import build_embed
from bot.utils.dbutils import update_booster


if TYPE_CHECKING:
    from bot.bot import BaseBot

_log = BotLogger("booster")


class BoosterExt(discord.Cog, ABCExtension):
    ENABLED = True

    def __init__(self, bot: BaseBot) -> None:
        self.bot = bot

    async def cog_before_invoke(self, ctx: discord.ApplicationContext) -> None:
        return await super().cog_before_invoke(ctx)

    @discord.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        boost_channel = self.bot.master_guild.get_channel(1219937225618227233)
        boost_role_after = after.get_role(self.bot.master_guild.premium_subscriber_role)
        boost_role_before = before.get_role(
            self.bot.master_guild.premium_subscriber_role
        )
        embed = build_embed(title="Booster notice!")
        if boost_role_after and boost_role_before is None:
            boost_slot = 20 - len(self.bot.master_guild.premium_subscribers)

            embed.description = (
                f"_{after.mention} has just boosted the server!_\n"
                + "Thank you for your boost!\n"
                + f"Booster reward slot: **{boost_slot if boost_slot >= 0 else 0} available**"
            )
            embed.colour = discord.Colour.nitro_pink()
            boost_channel.send(embed=embed)
            await update_booster(after.id, True)

        if boost_role_before and boost_role_after is None:
            embed.description = f"_{after.mention} stopped their server boost!_"
            embed.colour = discord.Colour.dark_red()
            boost_channel.send(embed=embed)
            await update_booster(after.id, False)

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
        embed = discord.Embed(
            title="Current valid booster reward", color=discord.Colour.nitro_pink()
        )
        embed.description = booster_text

        return await ctx.respond(
            f"_Currently **{len(boosters)}** members is boosting this server_",
            ephemeral=True,
            embed=embed,
        )
