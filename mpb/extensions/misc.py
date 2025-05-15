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
            "### Metal HUD Terminal Commands\n"
            + "Enable Metal HUD:\n"
            + "```/bin/launchctl setenv MTL_HUD_ENABLED 1```\n"
            + "Disable Metal HUD:\n"
            + "```/bin/launchctl unsetenv MTL_HUD_ENABLED```\n"
            + "`Fn + Shift + F9` to show/hide the Metal HUD once enabled\n"
            + "`Fn + Shift + F7` to move the Metal HUD around the screen\n\n"
            + "<:protip:1368106561045659678> **Pro Tip**: We recommend the [**Metal HUD FPS Count ↗**](https://discord.com/channels/1235385881586831451/1237550504846823425/1242331906146570351) App Shortcut as an easier solution to enabling/disabling the Metal HUD"
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
    name="videofaq",
    description="Guidelines for video recording for troubleshooting",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            ":red_circle: **Recording Guidelines for Support**: *If possible, please include a screen recording that shows:*\n"
            + "1. Opening CrossOver and your bottle settings\n"
            + "2. Launching the game platform (Steam, GOG, Epic, etc.)\n"
            + "3. Starting the game and any errors that appear\n\n"
            + ":bulb: **Tip**: *You can use QuickTime Player to record your screen—especially helpful if the issue happens in-game:*\n"
            + "1. Open QuickTime Player and go to `File`\n"
            + "2. Select `New Screen Recording` or press `⌘ + ⌃ + N`\n"
            + "3. If you have multiple displays, choose which one to record\n"
            + "4. Press `⌘ + ⌃ + Esc` to stop recording\n\n"
            + "<:protip:1368106561045659678> **MacProTip**: We recommend [**QuickRecorder**](https://lihaoyun6.github.io/quickrecorder/) - a **free open-source**, light-weight, powerful screen recorder for macOS\n"
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
