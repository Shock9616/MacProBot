#
# gaming.py
#
# The gaming extension for MacProBot. Contains commands related to Mac gaming
#

from difflib import SequenceMatcher
from typing import cast
import datetime as dt

import hikari as hk
import lightbulb as lb
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Tag, ResultSet, NavigableString

from ..constants import glossary

loader = lb.Loader()


@loader.command
class CxCheck(
    lb.SlashCommand,
    name="cxcheck",
    description="Get the searched game's star rating on the CrossOver Compatibility Database",
):
    # Options
    game: str = lb.string("game", "The name of the game to search for")

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        game_search = "+".join(self.game.split(" "))
        search_url = f"https://www.codeweavers.com/compatibility?browse=&app_desc=&company=&rating=&platform=&date_start=&date_end=&name={game_search}&search=app#results"
        search_page = requests.get(search_url)
        search_page_soup = bs(search_page.content, "html.parser")

        # Get list of app links
        app_list = search_page_soup.find(id="teTable-app")
        if type(app_list) is Tag:
            apps: ResultSet[Tag] = app_list.find_all("a")
        else:
            _ = await ctx.respond(
                f"Sorry, I couldn't find '{self.game}' in the CrossOver Compatibility Database.",
                flags=hk.MessageFlag.EPHEMERAL,
            )
            return

        # Find app with most similar name
        most_similar = 0
        most_similar_idx = 0
        idx = 0
        for app in apps:
            if type(app.string) is NavigableString:
                similarity = SequenceMatcher(None, app.string, self.game).ratio()
                if similarity > most_similar:
                    most_similar = similarity
                    most_similar_idx = idx
                idx += 1

        db_name = apps[most_similar_idx].string
        rel_link = apps[most_similar_idx]["href"]

        # Get page data
        game_page_url = f"https://www.codeweavers.com/{rel_link}"
        game_page = requests.get(game_page_url)
        soup = bs(game_page.content, "html.parser")

        # Find current star rating
        all_star_tables = soup.find_all("ul", class_="star-rating-table")
        star_table: Tag = cast(Tag, all_star_tables[0])

        # Count stars
        star_count = 0
        for star in star_table:
            if type(star) is Tag:
                try:
                    if star["class"] == ["active"]:
                        star_count += 1
                except KeyError:
                    break

        # Set rating description based on star count
        match star_count:
            case 1:
                rating_desc = "Will Not Install"
            case 2:
                rating_desc = "Installs, Will Not Run"
            case 3:
                rating_desc = "Limited Functionality"
            case 4:
                rating_desc = "Runs Well"
            case 5:
                rating_desc = "Runs Great"
            case _:
                rating_desc = "Unkown"

        # Create embed for the response
        embed = hk.Embed(
            title=db_name,
            colour=ctx.user.accent_colour,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )

        _ = embed.set_footer(
            text=f"Requested by {ctx.user.username}", icon=ctx.user.avatar_url
        )

        _ = embed.add_field(
            name="Rating",
            value=f"{':star:' * star_count} ({rating_desc})",
            inline=False,
        )

        _ = embed.add_field(
            value=f"[**Link ↗**]({game_page_url})",
            inline=False,
        )

        _ = await ctx.respond("", embed=embed)


async def define_autocomplete(ctx: lb.AutocompleteContext[str]):
    """Autocomplete Callback for the define command"""

    if type(ctx.focused.value) is not str:
        return

    current_value = ctx.focused.value or ""
    values_to_recommend = [
        key for key in glossary if key.startswith(current_value.lower())
    ]

    await ctx.respond(values_to_recommend)


@loader.command
class Define(
    lb.SlashCommand,
    name="define",
    description="Get a definition from a glossary of Mac gaming related terms",
):
    # Options
    term: str = lb.string(
        "term", "The term to get the definition of", autocomplete=define_autocomplete
    )

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        # Ensure that the argument passed is a string
        if type(self.term) is not str:
            return
        else:
            self.term = self.term.lower()  # Make search case-insensitive

        # Respond with definition for the requested term if it exists
        if self.term in glossary.keys():
            # Create embed for the response
            embed = hk.Embed(
                title=glossary[self.term]["name"],
                colour=ctx.user.accent_colour,
                timestamp=dt.datetime.now(dt.timezone.utc),
            )

            _ = embed.set_footer(
                text=f"Requested by {ctx.user.username}", icon=ctx.user.avatar_url
            )

            _ = embed.add_field(
                value=glossary[self.term]["def"],
                inline=False,
            )

            _ = embed.add_field(
                value=f"[**More Information ↗**]({glossary[self.term]['link']})"
            )

            _ = await ctx.respond("", embed=embed)
        else:
            _ = await ctx.respond(
                f"Sorry, I couldn't find a definition for '{self.term}'. Please check your spelling and try again.",
                flags=hk.MessageFlag.EPHEMERAL,
            )
