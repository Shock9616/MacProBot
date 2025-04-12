#
# __main__.py
#
# The launching point for the bot
#

from . import extensions

import hikari as hk
import lightbulb as lb
import dotenv

import os

_ = dotenv.load_dotenv()

bot = hk.GatewayBot(token=os.environ["TOKEN"], intents=hk.Intents.GUILD_MESSAGES)
client = lb.client_from_app(bot)


@bot.listen(hk.StartingEvent)
async def on_starting(_: hk.StartingEvent) -> None:
    await client.load_extensions_from_package(extensions)

    await client.start()


if __name__ == "__main__":
    bot.run()
