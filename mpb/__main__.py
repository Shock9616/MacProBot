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

_ = dotenv.load_dotenv()

bot = hk.GatewayBot(token=os.environ["TOKEN"], intents=hk.Intents.GUILD_MESSAGES)
client = lb.client_from_app(bot)

sassy_responses = [
    "beep boop",
    "just use a pc bro",
    "sry was using my steam deck. what's up?",
    "¡el baño está ocupado!",
    "how can mirrors be real if our eyes aren't real?",
    "mac gaming is lemons.",
    "oh let me guess, you're trying to run valorant again?",
    "pinging me won't make your macbook pro any more 'pro' at running games.",
    "i see you've chosen violence... or at least mild irriration. proceed.",
    "one more ping and i'll spin up the beachball of doom.",
    "if i had a dollar for every useless ping i get i could afford an actual gaming pc",
    "i'd say something helpful, but chaos is way more fun",
]


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
