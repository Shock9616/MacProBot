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
        _ = await ctx.respond(
            "**<:protip:1368106561045659678> <:crossover:1465953281661468722>  How to Install CrossOver**\n\n"
            + "CrossOver is the best way to run Windows only games on Mac. It allows you to run games using WINE, the Apple Game Porting Toolkit, DXMT and DXVK! Games with Anti-Cheat typically will not work.\n"
            + "You can try the **14 day free trial** without a credit card or payment!\n\n"
            + "Check out the [Video Guide for Beginners↗](<https://www.youtube.com/watch?v=KbJLOFBl42M>) (Recommended)\n"
            + "Download the [CrossOver Free Trial↗](<https://www.codeweavers.com/crossover/download?srsltid=AfmBOoqix6Ms8u2YJfeLJS2t9gcEc4yLzKeojKj_wumkcn2sslTvCs79>)\n"
            + "Check out the [CrossOver Compatibility Database↗](<https://www.codeweavers.com/compatibility?>)\n\n"
            + "**Purchasing CrossOver**\n"
            + "CrossOver is not a subscription! When you buy it, you keep the version you have. Your purchase includes 1 year of updates and support, so any new versions released during that time are yours too. After that year ends, the version of CrossOver you have is still yours to use.\n\n"
            + "**Tips and Tricks**\n"
            + "Cyber Monday is the best time to buy CrossOver with deals up to 75% OFF! You can also use Creator codes for 15% OFF year round!\n"
            + "[How to Use an External Drive with CrossOver↗](<https://www.youtube.com/watch?v=KbJLOFBl42M>)\n\n"
            + "[15% OFF Discount Code↗](<https://www.codeweavers.com/store?ad=1117;deal=GOMEO15>)"
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
class Piracy(
    lb.SlashCommand,
    name="piracy",
    description="Quick response for reminding people not to enable piracy",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        _ = await ctx.respond(
            "**We cannot provide support for pirated/cracked games and apps.** Asking for help with illegal files puts the entire server at risk of deletion under Discord's Terms of Service. Thanks!"
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
