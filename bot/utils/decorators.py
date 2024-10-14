import discord
from discord.ext import commands


def is_admin():
    """decorator to check if user who exectud command is admin\n
    including having these permission:
    1. administrator
    2. manage messages
    3. manage channels
    4. manage roles
    """

    async def pred(ctx: commands.Context | discord.ApplicationContext):
        user = ctx.author
        return isinstance(user, discord.Member) and any(
            (
                user.guild_permissions.administrator,
                user.guild_permissions.manage_messages,
                user.guild_permissions.manage_channels,
                user.guild_permissions.manage_roles,
            )
        )

    return commands.check(pred)
