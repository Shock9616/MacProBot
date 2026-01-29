#
# admin.py
#
# Extensions for commands only for server admins
#

import os
import re

import dotenv
import hikari as hk
import lightbulb as lb

_ = dotenv.load_dotenv()

loader = lb.Loader()


MESSAGE_LINK_RE = re.compile(
    r"https://(?:canary\.|ptb\.)?discord\.com/channels/\d+/(\d+)/(\d+)"
)


async def is_mod(member: hk.Member) -> bool:
    """Checks the member's roles to determine if they are a moderator"""
    for role in await member.fetch_roles():
        if role.name == "Mod" or role.name == "Admin":
            return True

    return False


@loader.command
class Announce(
    lb.SlashCommand,
    name="announce",
    description="Send a server announcement",
):
    # Options
    msg: hk.Attachment = lb.attachment(
        "message", "The message to send as an announcement"
    )

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Check if calling user is a mod
        if ctx.member is not None and not await is_mod(ctx.member):
            print(await ctx.member.fetch_roles())
            _ = await ctx.respond(
                "Sorry, you don't have permission to execute this command",
                ephemeral=True,
            )
            return

        announcements_channel = int(os.environ["ANNOUNCEMENTS_CHANNEL_ID"])
        mod_channel = int(os.environ["MOD_CHANNEL_ID"])

        if ctx.channel_id != mod_channel:
            _ = await ctx.respond(
                "Sorry, you can't use that command in this channel", ephemeral=True
            )
            return

        if self.msg.extension != "md" and self.msg.extension != "txt":
            _ = await ctx.respond(
                "Please provide either a markdown (`.md`) or a text (`.txt`) file",
                ephemeral=True,
            )
            return

        content = await self.msg.read()
        message = content.decode("utf-8")
        if len(message) <= 2000:
            _ = await ctx.client.rest.create_message(announcements_channel, message)
            _ = await ctx.respond("Announcement sent!")
        else:
            _ = await ctx.respond(
                "The provided message is too long. I can only "
                + "send announcements with 2000 characters or less. Please "
                + "shorten or split up the announcement",
                ephemeral=True,
            )


@loader.command
class EditAnnouncement(
    lb.SlashCommand,
    name="editannouncement",
    description="Edit a server announcement",
):
    # Options

    link: str = lb.string("link", "The link to the message to edit")
    msg: hk.Attachment = lb.attachment(
        "message", "The message to send as an announcement"
    )

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Check if calling user is a mod
        if ctx.member is not None and not await is_mod(ctx.member):
            print(await ctx.member.fetch_roles())
            _ = await ctx.respond(
                "Sorry, you don't have permission to execute this command",
                ephemeral=True,
            )
            return

        announcements_channel = int(os.environ["ANNOUNCEMENTS_CHANNEL_ID"])
        mod_channel = int(os.environ["MOD_CHANNEL_ID"])

        if ctx.channel_id != mod_channel:
            _ = await ctx.respond(
                "Sorry, you can't use that command in this channel", ephemeral=True
            )
            return

        if self.msg.extension != "md" and self.msg.extension != "txt":
            _ = await ctx.respond(
                "Please provide either a markdown (`.md`) or a text (`.txt`) file",
                ephemeral=True,
            )
            return

        content = await self.msg.read()
        message = content.decode("utf-8")

        match = MESSAGE_LINK_RE.match(self.link)
        if not match:
            _ = await ctx.respond(
                "Sorry, the provided link is invalid. Please try again with a valid link",
                ephemeral=True,
            )
            return

        channel_id = int(match.group(1))
        message_id = int(match.group(2))

        if len(message) <= 2000:
            _ = await ctx.client.rest.edit_message(channel_id, message_id, message)
            _ = await ctx.respond("Announcement edited!")
        else:
            _ = await ctx.respond(
                "The provided message is too long. I can only "
                + "send announcements with 2000 characters or less. Please "
                + "shorten or split up the announcement",
                ephemeral=True,
            )
