#
# misc.py
#
# Miscellaneous commands for the server
#

import os
import random
from collections.abc import Sequence

import dotenv
import hikari as hk
import lightbulb as lb

_ = dotenv.load_dotenv()

loader = lb.Loader()


@loader.command
class CrossOver(
    lb.SlashCommand,
    name="crossover",
    description="Instructions and tips for setting up and using CrossOver",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/crossover.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class MetalHud(
    lb.SlashCommand,
    name="metalhud",
    description="Instructions for setting up the MetalHUD toolbar shortcut",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/metalhud.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class Piracy(
    lb.SlashCommand,
    name="piracy",
    description="Quick response for reminding people not to enable piracy",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/piracy.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class Sikarugir(
    lb.SlashCommand,
    name="sikarugir",
    description="Useful links for learning about Sikarugir",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/sikarugir.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class Support(
    lb.SlashCommand,
    name="support",
    description="A quick form to fill out to help with game troubleshooting",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/support.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class UpdateDxmt(
    lb.SlashCommand,
    name="updatedxmt",
    description="Link to a quick tutorial on how to update DXMT in CrossOver",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/updatedxmt.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class ScreenRecord(
    lb.SlashCommand,
    name="screenrecord",
    description="Quick instructions for how to record your mac's screen",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/screenrecord.txt") as file:
            _ = await ctx.respond(file.read())


@loader.command
class Wallpaper(
    lb.SlashCommand,
    name="wallpaper",
    description="Randomly select a wallpaper from the #wallpapers channel",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Tell Discord that this command might take a while
        await ctx.defer()

        wallpapers_channel = int(os.environ["WALLPAPERS_CHANNEL_ID"])

        if ctx.channel_id == wallpapers_channel:
            _ = await ctx.respond(
                "To avoid creating duplicates, this command is disabled in the wallpapers channel",
            )
            return

        # Get a list of all messages in the wallpapers channel
        messages: Sequence[hk.Message] = await ctx.client.rest.fetch_messages(
            wallpapers_channel
        )

        message: hk.Message | None = None

        while message is None:
            # Select random message
            message = messages[random.randint(0, len(messages) - 1)]

            # Account for if the selected message has no wallpaper attached
            if len(message.attachments) == 0:
                message = None

        _ = await ctx.respond("", attachment=random.choice(message.attachments))


@loader.command
class Whisky(
    lb.SlashCommand,
    name="whisky",
    description="Quick information about Whisky being deprecated and alternatives",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        with open("mpb/info_cmd_msgs/whisky.txt") as file:
            _ = await ctx.respond(file.read())
