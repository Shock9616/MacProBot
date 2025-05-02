#
# admin.py
#
# Extensions for commands only for server admins
#

import hikari as hk
import lightbulb as lb

from hikari import Permissions

loader = lb.Loader()


mod_perms = (
    Permissions.KICK_MEMBERS
    | Permissions.BAN_MEMBERS
    | Permissions.MENTION_ROLES
    | Permissions.MANAGE_MESSAGES
    | Permissions.MANAGE_THREADS
    | Permissions.CREATE_EVENTS
    | Permissions.MANAGE_EVENTS
)


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
        if ctx.member is not None and (ctx.member.permissions & mod_perms) != mod_perms:
            _ = await ctx.respond(
                "Sorry, you don't have permission to execute this command",
                ephemeral=True,
            )
            return

        mod_channel = 1312991157264846898
        announcements_channel = 1366552674228506654

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
        _ = await ctx.client.rest.create_message(
            announcements_channel, content.decode("utf-8")
        )
        _ = await ctx.respond("Announcement sent!")
