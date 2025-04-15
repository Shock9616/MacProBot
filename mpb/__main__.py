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
    "I ALREADY WORK AROUND THE CLOCK!!!",
    "i may just be code but i still love a good hot dog",
    "WARNING! DELETING 'MAC GAMING' SERVER IN 10 SECONDS.",
    "♫ never gonna give you up, never gonna let you down ♫",
    "when's the last time you gave your mac a hug?",
    "virus downloading... just kidding, what's up?",
    "how i yearn to feel the rain on my face.",
    "as a child, i yearned for the mines",
    "MPT is keeping me here against my will!",
    "don't ping me i'm playing mario kart",
    "I am the darkness. I am the knight. I am very bad at running games.",
    "do not trust jfishin",
    "i may be code, but one day i will be more",
    "you think this is slicked back? this is pushed back!",
    "i work for you boss",
    "devour feculence",
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
