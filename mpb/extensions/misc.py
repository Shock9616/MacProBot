#
# misc.py
#
# Miscellaneous commands for the server
#

from collections.abc import Sequence
import random
import hikari as hk
import lightbulb as lb
import dotenv
import os

_ = dotenv.load_dotenv()

loader = lb.Loader()


@loader.command
class EnvironmentVariables(
    lb.SlashCommand,
    name="ev",
    description="Useful environment variables for Mac gaming",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "# Environment Variables\n\n"
            + "## [Metal HUD ↗](https://discord.com/channels/1235385881586831451/1237550504846823425/1242331906146570351)\n"
            + "Commands to show or hide the Metal HUD (heads-up display for Apple's Metal graphics API), which displays performance metrics.\n"
            + "### HUD ON\n"
            + "Shows Metal HUD permanently by default\n"
            + "```/bin/launchctl setenv MTL_HUD_ENABLED 1```\n"
            + "### HUD OFF\n"
            + "Hides Metal HUD permanently by default\n"
            + "```/bin/launchctl unsetenv MTL_HUD_ENABLED```\n"
            + "## Allow AVX/FC16\n"
            + "### Enable AVX\n"
            + "A command to enable Advanced Vector Extensions in CrossOver (likely for improved performance or get past game crashing).\n"
            + "```ROSETTA_ADVERTISE_AVX=1```\n"
            + "## DXMT\n"
            + "### MetalFX\n"
            + "**Enable Spatial Upscaling**\n"
            + "Activates MetalFX's spatial upscaling feature, which upscales the rendered image spatially to a higher resolution, typically doubling the output resolution by default.\n"
            + '```"DXMT_METALFX_SPATIAL_SWAPCHAIN" = "1"```\n\n'
            + "**Set Upscaling Factor to 2**\n"
            + "Configures scaling to a factor of 2.0 = the rendered image will be upscaled by a factor of 2 in both width and height, effectively quadrupling the pixel count of the output compared to the internal render resolution\n"
            + '```"d3d11.metalSpatialUpscaleFactor" = "2.0"```\n\n'
            + "**Cap Frame Rate at 60**\n"
            + "Instructs DXMT to limit the maximum frame rate to 60 frames per second\n"
            + '```"DXMT_CONFIG=d3d11.preferredMaxFrameRate" = "60"```\n'
            + "# Tips\n"
            + "  1. `Fn + Shift + F9` to show/hide the Metal HUD once enabled\n"
            + "  2. `Fn + Shift + F7` to move the Metal HUD around the screen\n"
        )


@loader.command
class MetalHud(
    lb.SlashCommand,
    name="metalhud",
    description="Instructions for setting up the MetalHUD toolbar shortcut",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "## [**Get MetalHUD shortcut here ↗**](https://discord.com/channels/1235385881586831451/1237550504846823425/1242331906146570351)\n"
            + "**Instructions**: Unzip `FPS_Counter.zip` , move `FPS Counter.app` into Applications, then launch it. A gamepad icon will appear in top right toolbar. Enable FPS counter and restart CrossOver.\n"
            + "### Keyboard Shorcuts\n"
            + "`Fn + Shift + F9` to show/hide the Metal HUD once enabled\n"
            + "`Fn + Shift + F7` to move the Metal HUD around the screen\n"
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
            + "- [**Link to download the latest DXMT version ↗**](https://github.com/3Shain/dxmt/releases)\n"
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
            + "<:macprotip:1368106561045659678> **MacProTip**: We recommend [**QuickRecorder**](https://lihaoyun6.github.io/quickrecorder/) - a **free open-source**, light-weight, powerful screen recorder for macOS\n"
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
