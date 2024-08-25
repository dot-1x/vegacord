from bot.bot import BaseBot
from database.core import config


def main():
    bot = BaseBot()
    bot.run(config.settings.TOKEN)


if __name__ == "__main__":
    main()
