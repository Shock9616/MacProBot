#
# services.py
#
# Extensible services class to add non-discord functionality to the bot
#

import datetime as dt
import random
import sqlite3

import lightbulb as lb
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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

        unix_time = int(date.timestamp())

        # Add to database
        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO reminders (user_id, channel_id, message, date)
            VALUES (?, ?, ?, ?)
        """,
            (user_id, channel_id, message, unix_time),
        )
        conn.commit()

        id = cursor.lastrowid

        # Schedule message
        self.scheduler.add_job(
            self.__send_reminder,
            "date",
            run_date=date,
            args=[id, user_id, channel_id, message],
            id=f"reminder-{id}",
        )

    def del_reminder(self, id: int) -> None:
        """Remove the reminder with the provided id from the database and unschedule it"""
        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reminders WHERE id = ?", (id,))
        conn.commit()

        self.scheduler.remove_job(f"reminder-{id}")

    def __load_reminders_from_db(self) -> None:
        """Retrieve all reminders from the database and remove old ones"""

        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                date INTEGER NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                timezone TEXT NOT NULL
            );
        """)

        cursor.execute("SELECT id, user_id, channel_id, message, date FROM reminders")
        conn.commit()

        for reminder in cursor.fetchall():
            id, user_id, channel_id, message, timestamp = reminder
            date = dt.datetime.fromtimestamp(timestamp)

            if date > dt.datetime.now():
                self.scheduler.add_job(
                    self.__send_reminder,
                    "date",
                    run_date=date,
                    args=[id, user_id, channel_id, message],
                    id=f"reminder-{id}",
                )
            else:
                # Send reminders that were supposed to be sent while bot was offline
                self.scheduler.add_job(
                    self.__send_reminder,
                    "date",
                    run_date=dt.datetime.now(),
                    args=[id, user_id, channel_id, message],
                    id=f"reminder-{id}",
                )

    async def __send_reminder(
        self, id: int, user_id: int, channel_id: int, message: str
    ) -> None:
        """Send reminder message and remove it from the database"""

        await self.bot.rest.create_message(
            channel_id,
            f"<@{user_id}> {random.choice(reminder_messages)}\n{message}",
            user_mentions=True,
        )

        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reminders WHERE id = ?", (id,))
        conn.commit()
