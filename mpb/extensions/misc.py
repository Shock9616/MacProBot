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
