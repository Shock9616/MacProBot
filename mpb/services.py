#
# services.py
#
# Extensible services class to add non-discord functionality to the bot
#

import datetime as dt
import random

import lightbulb as lb
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from mpb import dbutils
from mpb.constants import reminder_messages


class Services:
    def __init__(self, bot: lb.Client):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.__load_reminders_from_db()

    def add_reminder(
        self, user_id: int, channel_id: int, message: str, date: dt.datetime
    ) -> None:
        """Add a reminder to the database and schedule it to be sent"""
        id = dbutils.add_user_reminder(user_id, channel_id, message, date)

        # Schedule message
        self.scheduler.add_job(
            self.__send_reminder,
            "date",
            run_date=date,
            args=[id, user_id, channel_id, message],
            id=f"reminder-{id}",
        )

    def del_reminder(self, reminder_id: int) -> None:
        """Remove the reminder with the provided id from the database and unschedule it"""
        dbutils.del_user_reminder(reminder_id)

        self.scheduler.remove_job(f"reminder-{reminder_id}")

    def __load_reminders_from_db(self) -> None:
        """Retrieve all reminders from the database and remove old ones"""

        for reminder in dbutils.load_all_reminders():
            reminder_id, user_id, channel_id, message, timestamp = reminder
            date = dt.datetime.fromtimestamp(timestamp)

            if date > dt.datetime.now():
                self.scheduler.add_job(
                    self.__send_reminder,
                    "date",
                    run_date=date,
                    args=[reminder_id, user_id, channel_id, message],
                    id=f"reminder-{reminder_id}",
                )
            else:
                # Send reminders that were supposed to be sent while bot was offline
                self.scheduler.add_job(
                    self.__send_reminder,
                    "date",
                    run_date=dt.datetime.now(),
                    args=[reminder_id, user_id, channel_id, message],
                    id=f"reminder-{reminder_id}",
                )

    async def __send_reminder(
        self, reminder_id: int, user_id: int, channel_id: int, message: str
    ) -> None:
        """Send reminder message and remove it from the database"""

        await self.bot.rest.create_message(
            channel_id,
            f"<@{user_id}> {random.choice(reminder_messages)}\n{message}",
            user_mentions=True,
        )

        dbutils.del_user_reminder(reminder_id)
