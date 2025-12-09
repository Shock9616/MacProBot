#
# admin.py
#
# Extensions for commands only for server admins
#

import os
import random
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
        _ = await ctx.client.rest.create_message(
            announcements_channel, content.decode("utf-8")
        )
        _ = await ctx.respond("Announcement sent!")


@loader.command
class ChooseWinner(
    lb.SlashCommand,
    name="choosewinner",
    description="Select a random user who reacted to a message",
):
    # Options
    link: str = lb.string("message", "The message to choose a user from")

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

        match = MESSAGE_LINK_RE.match(self.link)
        if not match:
            _ = await ctx.respond(
                "Sorry, the provided link is invalid. Please try again with a valid link",
                ephemeral=True,
            )
            return

        channel_id = int(match.group(1))
        message_id = int(match.group(2))

        reactions = [
            r
            async for r in ctx.client.rest.fetch_reactions_for_emoji(
                channel_id, message_id, "🍎"
            )
        ]

        winner = random.choice(reactions)

        _ = await ctx.respond(
            f"Congratulations to {winner.mention} on winning the giveaway!"
        )
