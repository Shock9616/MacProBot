#
# dbutils.py
#
# Functions for interacting with the bot's database
#

import datetime as dt
import sqlite3
from zoneinfo import ZoneInfo


def set_user_timezone(user_id: int, tz: str) -> None:
    """Set the user's timezone in the database"""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (user_id, timezone) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET timezone = excluded.timezone
        """,
        (user_id, tz),
    )
    conn.commit()


def get_user_timezone(user_id: int) -> ZoneInfo | None:
    """Get the user's timezone, or return none if they haven't set one"""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timezone FROM users WHERE user_id = ?", (user_id,))

    timezone = cursor.fetchone()

    if not timezone:
        return None

    return ZoneInfo(timezone[0])


def get_user_reminders(user_id: int) -> list[tuple[int, int, int, str, int]] | None:
    """Get a list of the user's current reminders, or return none if they haven't set any"""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reminders WHERE user_id = ?", (user_id,))

    reminders = cursor.fetchall()

    if not reminders:
        return None

    return reminders


def add_user_reminder(
    user_id: int, channel_id: int, message: str, date: dt.datetime
) -> int | None:
    """Add a reminder to the database"""
    unix_time = int(date.timestamp())

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

    return cursor.lastrowid


def del_user_reminder(reminder_id: int) -> None:
    """Remove the reminder with the provided id from the database"""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()


def load_all_reminders() -> list[tuple[int, int, int, str, int]]:
    """Retrieve all stored reminders"""
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

    return cursor.fetchall()
