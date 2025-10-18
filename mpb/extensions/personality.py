#
# personality.py
#
# Sassy responses galore
#

import os
import random
import re
from collections.abc import Sequence

import hikari as hk
import lightbulb as lb
from openai import OpenAI

from ..constants import ai_prompt, sassy_responses, url_regex

loader = lb.Loader()


@loader.listener(hk.MessageCreateEvent)
async def on_bot_mentioned(event: hk.MessageCreateEvent):
    """Respond with a randomly selected response when pinged"""

    if not event.message or event.is_bot:
        return

    bot_user = await event.app.rest.fetch_my_user()  # needs to be a hikari.GatewayBot
    mentions = event.message.user_mentions_ids

    if not isinstance(mentions, Sequence):
        return

    if bot_user.id in (mention for mention in mentions):
        _ = await event.message.respond(random.choice(sassy_responses))


@loader.listener(hk.MessageCreateEvent)
async def on_message_created(event: hk.MessageCreateEvent):
    """Occasionally use AI to respond to a message unprompted"""

    if not event.message.content or event.is_bot:  # Ignore empty messages and bots
        return

    if (
        len(event.message.content.split()) > 8  # Longer than 8 words
        and not re.search(url_regex, event.message.content)  # No URLs
        and random.randint(0, 100) == 69  # 1/100 chance to respond
    ):
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
