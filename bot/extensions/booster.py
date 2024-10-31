from __future__ import annotations
from typing import TYPE_CHECKING

import discord
from discord import guild_only, option, slash_command

from bot.extensions.abcextension import ABCExtension
from bot.logs.custom_logger import BotLogger
from bot.utils.decorators import is_admin
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
        premium_role = self.bot.master_guild.premium_subscriber_role
        boost_role_after = after.get_role(premium_role.id)
        boost_role_before = before.get_role(premium_role.id)
        embed = build_embed(title="Booster notice!")
        if boost_role_after and boost_role_before is None:
            boost_slot = 20 - len(self.bot.master_guild.premium_subscribers)

            embed.description = (
                f"_{after.mention} has just boosted the server!_\n"
                + "Thank you for your boost!\n"
                + f"Booster reward slot: **{boost_slot if boost_slot >= 0 else 0} available**"
            )
            embed.colour = discord.Colour.nitro_pink()
            await boost_channel.send(embed=embed)
            await update_booster(after.id, True, after.premium_since)

        if boost_role_before and boost_role_after is None:
            embed.description = f"_{after.mention} stopped their server boost!_"
            embed.colour = discord.Colour.dark_red()
            await boost_channel.send(embed=embed)
            await update_booster(after.id, False, after.premium_since)

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
            title="Current booster", color=discord.Colour.nitro_pink()
        )
        embed.description = booster_text

        return await ctx.respond(
            f"_Currently **{len(boosters)}** members is boosting this server_",
            ephemeral=True,
            embed=embed,
        )

    @is_admin()
    @guild_only()
    @slash_command(
        name="register-booster",
        description="Register a member to booster list on database",
    )
    @option(
        name="member",
        type=discord.Member,
        description="Select member to register",
    )
    async def register_booster(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
        await ctx.defer(ephemeral=True)
        if member.get_role(ctx.interaction.guild.premium_subscriber_role.id) is None:
            return await ctx.respond("user is not valid booster", ephemeral=True)
        await update_booster(member.id, True, member.premium_since)
        await ctx.respond("sucessfully added user to booster database", ephemeral=True)

    @is_admin()
    @guild_only()
    @slash_command(
        name="remove-booster",
        description="Remove a member from booster list on database",
    )
    @option(
        name="member",
        type=discord.Member,
        description="Select member to remove",
    )
    async def remove_booster(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
        await ctx.defer(ephemeral=True)
        if member.get_role(ctx.interaction.guild.premium_subscriber_role.id):
            return await ctx.respond("user is still valid booster", ephemeral=True)
        await update_booster(member.id, False, member.premium_since)
        await ctx.respond(
            "sucessfully removed user from booster database", ephemeral=True
        )
