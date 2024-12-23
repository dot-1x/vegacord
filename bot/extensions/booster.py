from __future__ import annotations
from io import BytesIO
from typing import TYPE_CHECKING

import discord
from discord import guild_only, option, slash_command

from bot.extensions.abcextension import ABCExtension
from bot.logs.custom_logger import BotLogger
from bot.utils.decorators import is_admin
from bot.utils.misc import build_embed, convert_jakarta
from bot.utils.dbutils import (
    bulk_update_booster,
    get_valid_booster,
    update_booster,
)


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
            boosters = await get_valid_booster()
            boost_slot = 20 - len(boosters)
            embed.description = (
                f"_{after.mention} just boosted the server!_\n"
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
        description="Command to check server booster list and valid booster reward",
    )
    async def check_booster(self, ctx: discord.ApplicationContext):
        boosters = await get_valid_booster()
        fields = [
            discord.EmbedField(
                name=f"Booster {n+1}",
                value=(
                    f"> <@{member.userid}>\n"
                    + f"> boosted since: {member.boosting}\n"
                    + f"> expired since: {member.expired}"
                ),
                inline=True,
            )
            for n, member in enumerate(boosters)
        ]
        embed = discord.Embed(
            title="Current booster", color=discord.Colour.nitro_pink(), fields=fields
        )
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
    @option(
        name="force",
        type=bool,
        description="Force to remove even user is having booster role",
        default=False,
        required=False,
    )
    async def remove_booster(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        force: bool = False,
    ):
        await ctx.defer(ephemeral=True)
        if (
            member.get_role(ctx.interaction.guild.premium_subscriber_role.id)
            and not force
        ):
            return await ctx.respond("user is still valid booster", ephemeral=True)
        await update_booster(member.id, False, member.premium_since)
        await ctx.respond(
            "sucessfully removed user from booster database", ephemeral=True
        )

    @is_admin()
    @guild_only()
    @slash_command(
        name="update-booster",
        description="bulk update current booster list on database",
    )
    async def update_booster(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)
        boosters = ctx.interaction.guild.premium_subscribers
        await bulk_update_booster(
            [
                {
                    "userid": member.id,
                    "boosting_since": convert_jakarta(member.premium_since),
                    "isboosting": True,
                }
                for member in boosters
            ]
        )
        await ctx.respond("Successfully updated current booster list", ephemeral=True)

    @is_admin()
    @guild_only()
    @slash_command(
        name="get-booster-data", description="command to get booster data in csv"
    )
    async def get_booster_data(self, ctx: discord.ApplicationContext):
        members = await get_valid_booster(with_data=True)
        message = "\n".join(f"<@{user}>" for user in members["notfound"])
        embed = build_embed(
            message=f"data not found for {len(members['notfound'])} user(s)\n" + message
        )
        text = "userid,ign,server\n"
        boosters = "\n".join(
            [
                f"{member.userid},{member.ingame},{member.server}"
                for member in members["found"]
            ]
        )
        buffer = BytesIO((text + boosters).encode())
        file = discord.File(fp=buffer, filename="booster-data.csv")
        return await ctx.respond(embed=embed, ephemeral=True, file=file)
