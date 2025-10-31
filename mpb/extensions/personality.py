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
import requests
from openai import OpenAI

from ..constants import ai_prompt, fanfic, sassy_responses, url_regex

loader = lb.Loader()


@loader.listener(hk.MessageCreateEvent)
async def on_bot_mentioned(event: hk.MessageCreateEvent):
    """Respond with a randomly selected response when pinged"""

    if not event.message or event.is_bot:
        return

    bot_user = await event.app.rest.fetch_my_user()  # needs to be a hikari.GatewayBot
    mentions = event.message.user_mentions_ids
    referenced = event.message.referenced_message

    if referenced is not None and referenced.content == sassy_responses[43]:
        # Easter egg, reply with fanfic excerpt
        _ = await event.message.respond(
            f"Since you _insist_ on pinging me, here's a preview of the fanfic just to show that I'm not lying:\n\n{fanfic[0]}\nNow leave me alone"
        )
        return

    if not isinstance(mentions, Sequence):
        return

    if bot_user.id in (mention for mention in mentions):
        response = random.choice(sassy_responses)

        if response == sassy_responses[121]:
            # 'I have a wallpaper for u' response
            url = "https://wallpapercave.com/wp/wp2754931.jpg"
            image_data = requests.get(url, timeout=10)

            file = hk.Bytes(image_data.content, "xp.png")

            _ = await event.message.respond(response, attachment=file)
        else:
            _ = await event.message.respond(response)


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
