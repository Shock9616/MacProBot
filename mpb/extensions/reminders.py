#
# reminders.py
#
# Custom reminder functionality
#


import datetime as dt
import sqlite3
from zoneinfo import ZoneInfo, available_timezones

import dateparser as dp
import dotenv
import lightbulb as lb

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


async def timezone_autocomplete(ctx: lb.AutocompleteContext[str]):
    """Generate autocomplete list for settimezone"""
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
