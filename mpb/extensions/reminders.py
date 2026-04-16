#
# reminders.py
#
# Custom reminder functionality
#


import asyncio
import datetime as dt
import sqlite3
from zoneinfo import ZoneInfo, available_timezones

import dateparser as dp
import dotenv
import hikari as hk
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


class RemindersList(lb.components.Menu):
    def __init__(self, reminders: list[tuple[int, int, int, str, int]]):
        super().__init__()

        self.page = hk.Embed(title="Your Reminders")

        for i, r in enumerate(reminders):
            message = r[3]
            time = int(r[4])

            self.page.add_field(
                name=f"{i + 1}: {self.__to_discord_timestamp(dt.datetime.fromtimestamp(time))}",
                value=message,
                inline=False,
            )

    def __to_discord_timestamp(self, date: dt.datetime) -> str:
        return f"<t:{int(date.timestamp())}:F>"


@loader.command
class ListReminders(
    lb.SlashCommand,
    name="listreminders",
    description="Show a list of all your current reminders",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        reminders = self.__get_user_reminders(ctx.user.id)

        if not reminders:
            await ctx.respond("You have no currently set reminders", ephemeral=True)
            return

        reminders_list = RemindersList(reminders)

        await ctx.respond(
            "", embed=reminders_list.page, components=reminders_list, ephemeral=True
        )

        try:
            await reminders_list.attach(ctx.client, timeout=30)
        except asyncio.TimeoutError:
            pass

    def __get_user_reminders(
        self, user_id: int
    ) -> list[tuple[int, int, int, str, int]] | None:
        """Get a list of the user's current reminders, or return none if they haven't set any"""
        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reminders WHERE user_id = ?", (user_id,))

        reminders = cursor.fetchall()

        if not reminders:
            return None

        return reminders
