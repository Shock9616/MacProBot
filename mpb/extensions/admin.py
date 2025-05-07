#
# admin.py
#
# Extensions for commands only for server admins
#

import hikari as hk
import lightbulb as lb
import dotenv
import os

from hikari import Permissions

_ = dotenv.load_dotenv()

loader = lb.Loader()


mod_perms = (
    Permissions.MENTION_ROLES | Permissions.MANAGE_MESSAGES | Permissions.MANAGE_THREADS
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
        _ = await ctx.client.rest.create_message(
            announcements_channel, content.decode("utf-8")
        )
        _ = await ctx.respond("Announcement sent!")
