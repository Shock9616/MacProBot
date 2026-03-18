#
# misc.py
#
# Miscellaneous commands for the server
#

import datetime
import os
import random
from collections.abc import Sequence

import dotenv
import hikari as hk
import lightbulb as lb
from openai import OpenAI

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
class Summarize(
    lb.SlashCommand,
    name="summarize",
    description="Get a quick summary of the previous conversation in this channel",
):
    MAX_MESSAGES: int = 100

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Tell Discord that this command might take a while
        await ctx.defer()

        channel = await ctx.client.rest.fetch_channel(ctx.channel_id)

        if not isinstance(channel, hk.TextableChannel):
            return

        # Get messages to summarize
        messages = await self.__last_12_hours(channel)

        if len(messages) < 25:
            messages = await self.__last_100_messages(channel)

        # Create prompt and send to LLM for summarizing
        prompt = self.__create_prompt(
            channel.name if channel.name is not None else "Unnamed", messages
        )

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["AI_API_KEY"],
        )

        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={"reasoning": {"enabled": False}},
            model="z-ai/glm-4.5-air:free",
            messages=[{"role": "user", "content": prompt}],
        )

        response = completion.choices[0].message.content

        if response is not None:
            _ = await ctx.respond(response.strip('"'))

    async def __last_12_hours(self, channel: hk.TextableChannel) -> list[str]:
        """Return all messages from the last 12 hours in the specified channel"""
        after = datetime.datetime.now() - datetime.timedelta(hours=12)
        messages: list[str] = []

        async for msg in channel.fetch_history(after=after):
            # Get a list of all messages from the last 12 hours (capped at 100)
            if not msg.author.is_bot and msg.content is not None:
                messages.append(msg.content)

            if len(messages) >= self.MAX_MESSAGES:
                break

        return messages

    async def __last_100_messages(self, channel: hk.TextableChannel) -> list[str]:
        """Return the last 100 messages in the specified channel"""
        messages: list[str] = []

        async for msg in channel.fetch_history():
            # Get a list of the last 100 messages instead
            if not msg.author.is_bot and msg.content is not None:
                messages.append(msg.content)

            if len(messages) >= self.MAX_MESSAGES:
                break

        return messages

    def __create_prompt(self, channel_name: str, messages: list[str]) -> str:
        """Format the messages into a prompt for the LLM"""
        prompt = f"""Please briefly summarize these messages from the {channel_name} channel on the Mac Gaming discord server
            Refrain from making any comments or suggestions. Only respond with the summary and nothing more
            Keep the summary brief. Ideally in at most 5 short bullet points
            Focus on the most recent messages. If there is a break where time has clearly passed and users are talking about something else, summarize that and mostly ignore everything else.
            The messages are listed in reverse chronological order with the most recent ones first\n
            """

        prompt += "\n".join(messages)

        return prompt


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
