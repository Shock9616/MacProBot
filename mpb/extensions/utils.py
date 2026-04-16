#
# utils.py
#
# Commands that provide some useful non-gaming utility for the server
#

import asyncio
import datetime as dt
import os
import sqlite3
from zoneinfo import ZoneInfo, available_timezones

import dateparser as dp
import dotenv
import hikari as hk
import lightbulb as lb
import openai
from openai import OpenAI

from mpb.services import Services

_ = dotenv.load_dotenv()

loader = lb.Loader()

# Pre-calculated timezone data for timezone autocomplete
TIMEZONES = sorted(available_timezones())
TZ_DATA = []
for tz in TIMEZONES:
    tz_lower = tz.lower()
    city = tz.split("/")[-1].replace("_", " ").lower()

    TZ_DATA.append((tz, tz_lower, city))


@loader.command
class RemindMe(
    lb.SlashCommand,
    name="remindme",
    description="Set a reminder to be sent in this channel",
):
    message: str = lb.string("reminder", "What do you want to be reminded of?")
    time: str = lb.string("when", "When should I remind you?")

    @lb.invoke
    async def invoke(self, ctx: lb.Context, services: Services):
        user_id = ctx.user.id
        channel_id = ctx.channel_id

        timezone = self.__get_user_timezone(user_id)

        if not timezone:
            await ctx.respond(
                "No timezone specified. Please use `/settimezone` to set your timezone before using this command.",
                ephemeral=True,
            )
            return

        date: dt.datetime = dp.parse(
            self.time,
            settings={
                "TIMEZONE": str(timezone),
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
            },
        )

        date = date.astimezone(dt.timezone.utc)

        services.add_reminder(user_id, channel_id, self.message, date)

        await ctx.respond(
            f"Got it! I will send the message '{self.message}' on {self.__to_discord_timestamp(date)}"
        )

    def __to_discord_timestamp(self, date: dt.datetime) -> str:
        return f"<t:{int(date.timestamp())}:F>"

    def __get_user_timezone(self, user_id: int) -> ZoneInfo | None:
        """Get the user's timezone, or return none if they haven't set one"""
        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute("SELECT timezone FROM users WHERE user_id = ?", (user_id,))

        timezone = cursor.fetchone()

        if not timezone:
            return None

        return ZoneInfo(timezone[0])


async def timezone_autocomplete(ctx: lb.AutocompleteContext[str]):
    if not isinstance(ctx.focused.value, str):
        return

    query = ctx.focused.value.lower() if ctx.focused.value else ""

    contains = []

    for tz, tz_lower, city in TZ_DATA:
        if query in tz_lower or query in city:
            contains.append(tz)

    results = contains[:25]

    await ctx.respond(results)


@loader.command
class SetTimeZone(
    lb.SlashCommand,
    name="settimezone",
    description="Set the timezone to use when you run /remindme",
):
    timezone: str = lb.string(
        "timezone", "The timezone to set", autocomplete=timezone_autocomplete
    )

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        if self.timezone not in TIMEZONES:
            await ctx.respond(
                "Please enter a valid timezone (e.x. `America/New_York`)",
                ephemeral=True,
            )
            return

        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (user_id, timezone) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET timezone = excluded.timezone
            """,
            (ctx.user.id, self.timezone),
        )
        conn.commit()

        await ctx.respond(
            f"Ok! I have set your timezone to {self.timezone}!", ephemeral=True
        )


@loader.command
class Summarize(
    lb.SlashCommand,
    name="summarize",
    description="Get a quick summary of the previous conversation in this channel",
):
    MAX_MESSAGES: int = 300

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Tell Discord that this command might take a while
        await ctx.defer()

        try:
            channel = await ctx.client.rest.fetch_channel(ctx.channel_id)

            if not isinstance(channel, hk.TextableChannel):
                return

            # Get messages to summarize
            messages = await self.__last_12_hours(channel)

            if len(messages) < 100:
                messages = await self.__last_300_messages(channel)

            # Create prompt and send to LLM for summarizing
            prompt = self.__create_prompt(
                channel.name if channel.name is not None else "Unnamed", messages
            )

            response = await asyncio.wait_for(
                asyncio.to_thread(self.__generate_summary, prompt), timeout=42
            )

            if response is not None:
                _ = await ctx.respond(response.strip('"'))
        except openai.RateLimitError:
            _ = await ctx.respond(
                "Unfortunately this command has been rate-limited. Please try again later",
            )
        except asyncio.TimeoutError:
            _ = await ctx.respond(
                "Generating a summary took too long. Please try again",
            )

    async def __last_12_hours(self, channel: hk.TextableChannel) -> list[str]:
        """Return all messages from the last 12 hours in the specified channel"""
        after = dt.datetime.now() - dt.timedelta(hours=12)
        messages: list[str] = []

        async for msg in channel.fetch_history(after=after):
            # Get a list of all messages from the last 12 hours (capped at 100)
            if not msg.author.is_bot and msg.content is not None:
                messages.append(msg.content)

            if len(messages) >= self.MAX_MESSAGES:
                break

        return messages

    async def __last_300_messages(self, channel: hk.TextableChannel) -> list[str]:
        """Return the last 300 messages in the specified channel"""
        messages: list[str] = []

        async for msg in channel.fetch_history():
            # Get a list of the last 100 messages instead
            if not msg.author.is_bot and msg.content is not None:
                messages.append(msg.content)

            if len(messages) >= self.MAX_MESSAGES:
                break

        return messages

    def __create_prompt(self, channel_name: str, messages: list[str]) -> str:
        """Format the messages into a prompt for the LLM"""
        prompt = f"""You are a chat summarizer for the Mac Gaming Discord server.
            **Input:**
            - A list of {len(messages)} messages from the {channel_name} channel
            - Messages are in reverse chronological order, most recent first

            **Output rules:**
            - Respond with bullet points only
            - No preamble, comments, or suggestions
            - Order bullets chronologically — earliest topic first, most recent last
            - One bullet per distinct topic or thread
            - Aim for no more than 8 bullets, but use your judgement
            - Do not pad — if there are only 2 topics, write 2 bullets

            **What to summarize:**
            - Substantive discussion and decisions
            - New threads that emerge after a clear time gap or topic shift

            **What to ignore:**
            - One-word replies and reactions
            - Spam
            - Low-signal filler content unless it's central to the conversation
            - Messages that may be potentially embarassing or personal
            - Arguments between users
            - Messages mentioning personal details like medical diagnoses
            - Derogatory language and name calling
        """

        prompt += "\n".join(messages)

        return prompt

    def __generate_summary(self, prompt: str) -> str | None:
        """Send the provided prompt to an LLM to generate a summary"""

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["AI_API_KEY"],
        )

        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={"reasoning": {"enabled": False}},
            model="z-ai/glm-4.5-air:free",
            messages=[{"role": "user", "content": prompt}],
        )

        return completion.choices[0].message.content
