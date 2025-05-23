#
# __main__.py
#
# The launching point for the bot
#

import os
import random
from collections.abc import Sequence

import dotenv
import hikari as hk
import lightbulb as lb
from openai import OpenAI

from . import extensions
from .constants import ai_prompt, sassy_responses

_ = dotenv.load_dotenv()

# Create/setup bot
bot = hk.GatewayBot(
    token=os.environ["TOKEN"],
    intents=(hk.Intents.GUILD_MESSAGES | hk.Intents.MESSAGE_CONTENT),
)
client = lb.client_from_app(bot)


@bot.listen(hk.StartingEvent)
async def on_starting(_: hk.StartingEvent) -> None:
    """Load bot extensions on startup"""

    await client.load_extensions_from_package(extensions)

    await client.start()


@bot.listen(hk.MessageCreateEvent)
async def on_bot_mentioned(event: hk.MessageCreateEvent):
    """Respond with a randomly selected response when pinged"""

    if not event.message or event.is_bot:
        return

    bot_user = bot.get_me()
    mentions = event.message.user_mentions_ids

    if bot_user is None or not isinstance(mentions, Sequence):
        return

    if bot_user.id in (mention for mention in mentions):
        _ = await event.message.respond(random.choice(sassy_responses))


@bot.listen(hk.MessageCreateEvent)
async def on_message_created(event: hk.MessageCreateEvent):
    """Occasionally use AI to respond to a message unprompted"""

    if not event.message.content or event.is_bot:  # Ignore empty messages and bots
        return

    if len(event.message.content.split()) > 8 and random.randint(0, 100) == 69:
        # Respond to ~1/100 messages that are more than 8 words long

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["AI_API_KEY"],
        )

        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "developer", "content": ai_prompt},
                {
                    "role": "user",
                    "content": event.message.content,
                },
            ],
        )

        response = completion.choices[0].message.content

        if response is not None:
            _ = await event.message.respond(response.strip('"'))


if __name__ == "__main__":
    bot.run()
