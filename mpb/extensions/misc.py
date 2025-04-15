#
# misc.py
#
# Miscellaneous commands for the server
#

import lightbulb as lb

loader = lb.Loader()


@loader.command
class HelpForm(
    lb.SlashCommand,
    name="helpform",
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
class UpdateDxmt(
    lb.SlashCommand,
    name="updatedxmt",
    description="Reply with a link to a quick tutorial on how to update DXMT in CrossOver",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond("https://www.youtube.com/watch?v=5uIEd-6DqFM")


@loader.command
class EnvironmentVariables(
    lb.SlashCommand,
    name="environmentvariables",
    description="Reply with some useful environment variables for Mac gaming",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "**Metal HUD**\n\n"
            + "__HUD ON__\n"
            + "/bin/launchctl setenv MTL_HUD_ENABLED 1\n\n"
            + "__HUD OFF__\n"
            + "/bin/launchctl setenv MTL_HUD_ENABLED 0\n\n"
            + "**Allow AVK/FC16**\n\n"
            + "ROSETTA_ADVERTISE_AVX=1\n\n"
            + "**DXMT**\n\n"
            + "__MetalFX__\n"
            + '"DXMT_METALFX_SPATIAL_SWAPCHAIN" = "1"\n'
            + '"d3d11.metalSpatialUpscaleFactor" = "2.0"\n\n'
            + "__Frame Rate Cap__\n"
            + '"DXMT_CONFIG=d3d11.preferredMaxFrameRate" = "60"'
        )


@loader.command
class EnvironmentVariablesAlias(
    lb.SlashCommand,
    name="ev",
    description="Reply with some useful environment variables for Mac gaming",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "**Metal HUD**\n\n"
            + "__HUD ON__\n"
            + "/bin/launchctl setenv MTL_HUD_ENABLED 1\n\n"
            + "__HUD OFF__\n"
            + "/bin/launchctl setenv MTL_HUD_ENABLED 0\n\n"
            + "**Allow AVK/FC16**\n\n"
            + "ROSETTA_ADVERTISE_AVX=1\n\n"
            + "**DXMT**\n\n"
            + "__MetalFX__\n"
            + '"DXMT_METALFX_SPATIAL_SWAPCHAIN" = "1"\n'
            + '"d3d11.metalSpatialUpscaleFactor" = "2.0"\n\n'
            + "__Frame Rate Cap__\n"
            + '"DXMT_CONFIG=d3d11.preferredMaxFrameRate" = "60"'
        )
