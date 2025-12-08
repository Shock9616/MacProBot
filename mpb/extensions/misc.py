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
class MetalHud(
    lb.SlashCommand,
    name="metalhud",
    description="Instructions for setting up the MetalHUD toolbar shortcut",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "**<:protip:1368106561045659678> How to Enable the Metal HUD on Mac**\n"
            + "IMPORTANT: Make sure both your launcher (Steam, CrossOver, etc.) and your game are fully closed before enabling or disabling the HUD.\n\n"
            + "**Terminal Commands**\n\n"
            + "Enable Metal HUD:\n"
            + "```/bin/launchctl setenv MTL_HUD_ENABLED 1```\n\n"
            + "Disable Metal HUD:\n"
            + "```/bin/launchctl unsetenv MTL_HUD_ENABLED```\n\n"
            + "**MetalHUDMenu Menu Bar App**\n\n"
            + "We highly recommend using MetalHUDMenu to enable and customize the Metal HUD system wide!\n"
            + "[**MetalHUDMenu ↗**](<https://github.com/Jfishin/MetalHUDmenu>)\n"
            + "[**Guide ↗**](<https://youtu.be/SDs3xhA2Ufo>)\n\n"
            + "**Metal HUD Keyboard Shortcuts**\n\n"
            + "`Fn + Shift + F9` to show/hide the Metal HUD once enabled\n"
            + "`Fn + Shift + F7` to move the Metal HUD around the screen\n"
            + "`Fn + Shift + F12` to customize the HUD\n\n"
            + "<:protip:1368106561045659678> Pro Tip: You can triple click the HUD to get the customization controls!"
        )


@loader.command
class Sikarugir(
    lb.SlashCommand,
    name="sikarugir",
    description="Useful links for learning about Sikarugir",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "[Sikarugir Beginners Guide Tutorial ↗](<https://youtu.be/pCgYxRPIqjE?si=Fb-5RUywgu9BLo40>)\n"
            + "[Link to download Sikarugir ↗](<https://github.com/Sikarugir-App/Sikarugir>)\n"
        )


@loader.command
class Support(
    lb.SlashCommand,
    name="support",
    description="A quick form to fill out to help with game troubleshooting",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "🔧 Automated response!\n"
            + "**To help troubleshoot your issue, please provide the following details:**\n"
            + "macOS version:\n"
            + "Mac model:\n"
            + "Memory (RAM):\n"
            + "CrossOver version:\n"
            + "Game platform (Steam, GOG, other):\n"
        )


@loader.command
class UpdateDxmt(
    lb.SlashCommand,
    name="updatedxmt",
    description="Link to a quick tutorial on how to update DXMT in CrossOver",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "- [**How to update DXMT inside CrossOver ↗**](https://www.youtube.com/watch?v=5uIEd-6DqFM)\n"
            + "- [**Link to download the latest DXMT version ↗**](<https://github.com/3Shain/dxmt/releases>)\n"
        )


@loader.command
class VideoFaq(
    lb.SlashCommand,
    name="screenrecord",
    description="Quick instructions for how to record your mac's screen",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "**<:protip:1368106561045659678> How to Record Gameplay/Desktop on a Mac**\n\n"
            + "**1. QuickTime Player (NO AUDIO)**\n"
            + "Open QuickTime Player and go to File\n"
            + "Select New Screen Recording or press `⌘ + ⌃ + N`\n"
            + "If you have multiple displays, choose which one to record\n"
            + "Press `⌘ + ⌃ + Esc` to stop recording\n\n"
            + "**2. Quick Recorder App (YES AUDIO)**\n"
            + "A free, open-source, light-weight, powerful screen recorder for macOS.\n"
            + "Download [Quick Recorder↗](https://lihaoyun6.github.io/quickrecorder/)"
        )


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
