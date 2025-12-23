#
# __main__.py
#
# The launching point for the bot
#

import os

import dotenv
import hikari as hk
import lightbulb as lb

from . import extensions

_ = dotenv.load_dotenv()

# Create/setup bot
bot = hk.GatewayBot(
    token=os.environ["TOKEN"],
    intents=(
        hk.Intents.GUILD_MESSAGES
        | hk.Intents.MESSAGE_CONTENT
        | hk.Intents.GUILD_MEMBERS
    ),
)
client = lb.client_from_app(bot)


@bot.listen(hk.StartingEvent)
async def on_starting(_: hk.StartingEvent) -> None:
    """Load bot extensions on startup"""

    await client.load_extensions_from_package(extensions)

    await client.start()


if __name__ == "__main__":
    bot.run()
