#
# misc.py
#
# Miscellaneous commands for the server
#

import hikari as hk
import lightbulb as lb

loader = lb.Loader()


@loader.command
class Help(
    lb.SlashCommand,
    name="help",
    description="Shows help info and commands",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Create embed for the response
        embed = hk.Embed(
            title="MacProBot Help",
            colour=ctx.user.accent_colour,
        )

        _ = embed.add_field(value="Here is a list of the currently available commands")

        _ = embed.add_field(
            name="`/cxcheck <game name>`",
            value="Quickly check the CodeWeavers compatibility database",
            inline=False,
        )

        _ = embed.add_field(
            name="`/define <term>`",
            value="Get a quick definition for the given Mac gaming related term",
            inline=False,
        )

        _ = embed.add_field(
            name="`/ev`",
            value="Lists common CrossOver bottle environment variables",
            inline=False,
        )

        _ = embed.add_field(
            name="`/metalhud`",
            value="Lists some helpful utilities/instructions for the Metal HUD",
            inline=False,
        )

        _ = embed.add_field(
            name="`/support`",
            value="Lists helpful info for troubleshooting issues",
            inline=False,
        )

        _ = embed.add_field(
            name="`/support1`",
            value="Gives some helpful tips for recording footage for troubleshooting",
            inline=False,
        )

        _ = embed.add_field(
            name="`/updatedxmt`",
            value="Link to a tutorial and download for updating DXMT",
            inline=False,
        )

        # Response is only visible to the user that ran the command
        _ = await ctx.respond("", embed=embed, flags=hk.MessageFlag.EPHEMERAL)


@loader.command
class Support(
    lb.SlashCommand,
    name="support",
    description="Reply with a quick form to fill out to help with game troubleshooting",
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
class Support1(
    lb.SlashCommand,
    name="support1",
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
            + "4. Press `⌘ + ⌃ + Esc` to stop recording\n"
        )


@loader.command
class UpdateDxmt(
    lb.SlashCommand,
    name="updatedxmt",
    description="Reply with a link to a quick tutorial on how to update DXMT in CrossOver",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "- [**How to update DXMT inside CrossOver ↗**](https://www.youtube.com/watch?v=5uIEd-6DqFM)\n"
            + "- [**Link to download the latest DXMT version ↗**](https://github.com/3Shain/dxmt/releases)\n"
        )


@loader.command
class EnvironmentVariables(
    lb.SlashCommand,
    name="ev",
    description="Reply with some useful environment variables for Mac gaming",
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
    description="Reply with instructions for setting up the MetalHUD toolbar shortcut",
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
