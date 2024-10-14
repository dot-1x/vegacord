from discord import Bot, Intents

from logs.log import get_logger

_log = get_logger("BOT")


class BaseBot(Bot):
    def __init__(self):
        intent = Intents()
        intent.members = True
        intent.guilds = True
        intent.message_content = True
        intent.guild_messages = True
        intent.dm_messages = True
        intent.voice_states = True
        super().__init__(
            "Dr. Vegapunk helper bot for Pirates Heroes official discord server",
            intents=intent,
            help_command=None,
        )
        # self.load_extension("bot.events")
        self.load_extension("bot.extensions")

    @property
    def master_guild(self):
        return self.get_guild(1219937222661509121)

    async def on_ready(self):
        _log.info("Logged in as: %s", self.user.name)
