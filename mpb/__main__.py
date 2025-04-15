#
# __main__.py
#
# The launching point for the bot
#

from typing_extensions import Sequence
from . import extensions

import hikari as hk
import lightbulb as lb
import dotenv

import os
import random

from .constants import sassy_responses

_ = dotenv.load_dotenv()

bot = hk.GatewayBot(token=os.environ["TOKEN"], intents=hk.Intents.GUILD_MESSAGES)
client = lb.client_from_app(bot)


@bot.listen(hk.StartingEvent)
async def on_starting(_: hk.StartingEvent) -> None:
    await client.load_extensions_from_package(extensions)

    await client.start()


@bot.listen(hk.MessageCreateEvent)
async def on_bot_mentioned(event: hk.MessageCreateEvent):
    if not event.message or event.is_bot:
        return

    bot_user = bot.get_me()
    mentions = event.message.user_mentions_ids

    if bot_user is None or not isinstance(mentions, Sequence):
        return

    if bot_user.id in (mention for mention in mentions):
        _ = await event.message.respond(random.choice(sassy_responses))


if __name__ == "__main__":
    bot.run()
