#
# utils.py
#
# Commands that provide some useful non-gaming utility for the server
#

import asyncio
import datetime as dt
import os

import dotenv
import hikari as hk
import lightbulb as lb
import openai
import requests
from bs4 import BeautifulSoup as bs
from openai import OpenAI

_ = dotenv.load_dotenv()

loader = lb.Loader()


@loader.command
class News(lb.SlashCommand, name="news", description="Make a post in the news channel"):
    title: str = lb.string("title", "Title of the news post")
    link: str = lb.string("link", "The link to the news source")

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        news_channel = int(os.environ["NEWS_CHANNEL_ID"])

        if ctx.channel_id != news_channel:
            await ctx.respond(
                f"Sorry, this command can only be run in <#{news_channel}>",
                ephemeral=True,
            )
            return

        embed = hk.Embed(
            title=self.title,
            url=self.link,
            description=self.__get_description(self.link),
        )
        embed.set_footer(f"Shared by {self.__get_name(ctx.user)}")
        embed.set_image(self.__get_image_link(self.link))

        await ctx.respond("", embed=embed)

        thread = await ctx.client.rest.create_thread(
            ctx.channel_id, hk.ChannelType.GUILD_PUBLIC_THREAD, self.title
        )
        await ctx.client.rest.create_message(thread, self.link)

    def __get_page(self, url: str) -> bs:
        """Return parsed page data for the given URL"""
        page = requests.get(url)
        return bs(page.content, "html.parser")

    def __get_image_link(self, url: str) -> str | None:
        """Return a link to the link's thumbnail image"""
        soup = self.__get_page(url)
        og_image = soup.find("meta", property="og:image")
        image_url = og_image["content"] if og_image else None

        if isinstance(image_url, str):
            return image_url

    def __get_description(self, url: str) -> str | None:
        """Return the description of the link's content"""
        soup = self.__get_page(url)
        desc = soup.find("meta", property="og:description")
        desc_str = desc["content"] if desc else None

        if isinstance(desc_str, str):
            return desc_str

    def __get_name(self, user: hk.User) -> str:
        """Return either the user's display name or their username"""
        name = user.display_name

        if not isinstance(name, str):
            name = user.username

        return name


@loader.command
class Summarize(
    lb.SlashCommand,
    name="summarize",
    description="Get a quick summary of the previous conversation in this channel",
):
    MAX_MESSAGES: int = 300

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Tell Discord that this command might take a while
        await ctx.defer()

        try:
            channel = await ctx.client.rest.fetch_channel(ctx.channel_id)

            if not isinstance(channel, hk.TextableChannel):
                return

            # Get messages to summarize
            messages = await self.__last_12_hours(channel)

            if len(messages) < 100:
                messages = await self.__last_300_messages(channel)

            # Create prompt and send to LLM for summarizing
            prompt = self.__create_prompt(
                channel.name if channel.name is not None else "Unnamed", messages
            )

            response = await asyncio.wait_for(
                asyncio.to_thread(self.__generate_summary, prompt), timeout=42
            )

            if response is not None:
                _ = await ctx.respond(response.strip('"'))
        except openai.RateLimitError:
            _ = await ctx.respond(
                "Unfortunately this command has been rate-limited. Please try again later",
            )
        except asyncio.TimeoutError:
            _ = await ctx.respond(
                "Generating a summary took too long. Please try again",
            )

    async def __last_12_hours(self, channel: hk.TextableChannel) -> list[str]:
        """Return all messages from the last 12 hours in the specified channel"""
        after = dt.datetime.now() - dt.timedelta(hours=12)
        messages: list[str] = []

        async for msg in channel.fetch_history(after=after):
            # Get a list of all messages from the last 12 hours (capped at 100)
            if not msg.author.is_bot and msg.content is not None:
                messages.append(msg.content)

            if len(messages) >= self.MAX_MESSAGES:
                break

        return messages

    async def __last_300_messages(self, channel: hk.TextableChannel) -> list[str]:
        """Return the last 300 messages in the specified channel"""
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
        prompt = f"""You are a chat summarizer for the Mac Gaming Discord server.
            **Input:**
            - A list of {len(messages)} messages from the {channel_name} channel
            - Messages are in reverse chronological order, most recent first

            **Output rules:**
            - Respond with bullet points only
            - No preamble, comments, or suggestions
            - Order bullets chronologically — earliest topic first, most recent last
            - One bullet per distinct topic or thread
            - Aim for no more than 8 bullets, but use your judgement
            - Do not pad — if there are only 2 topics, write 2 bullets

            **What to summarize:**
            - Substantive discussion and decisions
            - New threads that emerge after a clear time gap or topic shift

            **What to ignore:**
            - One-word replies and reactions
            - Spam
            - Low-signal filler content unless it's central to the conversation
            - Messages that may be potentially embarassing or personal
            - Arguments between users
            - Messages mentioning personal details like medical diagnoses
            - Derogatory language and name calling
        """

        prompt += "\n".join(messages)

        return prompt

    def __generate_summary(self, prompt: str) -> str | None:
        """Send the provided prompt to an LLM to generate a summary"""

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["AI_API_KEY"],
        )

        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={"reasoning": {"enabled": False}},
            model="google/gemma-4-31b-it:free",
            messages=[{"role": "user", "content": prompt}],
        )

        return completion.choices[0].message.content
