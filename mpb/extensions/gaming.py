#
# gaming.py
#
# The gaming extension for MacProBot. Contains commands related to Mac gaming
#

from difflib import SequenceMatcher
from enum import Enum
from typing import cast

import hikari as hk
import lightbulb as lb
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString, ResultSet, Tag

from ..constants import glossary

loader = lb.Loader()


@loader.command
class AgwCheck(
    lb.SlashCommand,
    name="agwcheck",
    description="Get the compatibility ratings for the searched game from AppleGamingWiki",
):
    # Options
    game: str = lb.string("game", "The name of the game to search for")

    class PageType(Enum):
        GamePage = 1
        SearchResults = 2
        GameNotFound = 3

    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        game_search = "+".join(self.game.split(" "))
        url = f"https://www.applegamingwiki.com/w/index.php?search={game_search}&title=Special:Search"
        soup = self.__get_page(url)

        # Determine the page type (game page, search results, game not found)
        # and react accordingly
        page_type = self.__get_page_type(soup)

        if page_type == self.PageType.GameNotFound:
            _ = await self.__resp_no_game(self.game, ctx)
            return
        elif page_type == self.PageType.SearchResults:
            # Since we got a search results page, we need to find the page for the game the user wants
            results = cast(
                ResultSet[Tag],
                soup.find_all("div", {"class": "mw-search-result-heading"}),
            )

            # Get link to page with the most similar name to the user's search
            game_tag = self.__find_most_similar(self.game, results)
            rel_link_a = cast(Tag, game_tag.find("a"))
            rel_link = rel_link_a["href"]

            # Get new page data
            url = f"https://applegamingwiki.com{rel_link}"
            soup = self.__get_page(url)

        # Now that we know we're on the game's page...
        compat_table = cast(Tag, soup.find("table", {"id": "table-compatibility"}))
        data_rows = cast(
            ResultSet[Tag],
            compat_table.find_all(
                "tr", {"class": "template-infotable-body table-compatibility-body-row"}
            ),
        )

        # Get proper game title
        game_name_header = cast(Tag, soup.find("h1", {"class": "article-title"}))
        title = cast(NavigableString, game_name_header.string)

        compat_data = self.__get_compat_data(data_rows)

        _ = await ctx.respond(
            "", embed=self.__build_embed(title, compat_data, url, ctx)
        )

    def __get_page(self, url: str) -> bs:
        """Return parsed page data for the given URL"""
        page = requests.get(url)
        return bs(page.content, "html.parser")

    def __get_page_type(self, soup: bs) -> PageType:
        """Identify the type of page contained in soup"""
        if type(soup.find("table", {"id": "table-compatibility"})) is Tag:
            return self.PageType.GamePage
        elif type(soup.find("p", {"class": "mw-search-nonefound"})) is Tag:
            return self.PageType.GameNotFound
        else:
            return self.PageType.SearchResults

    def __find_most_similar(self, game: str, results: ResultSet[Tag]) -> Tag:
        """Find the search result with the most similar name to the user's search"""
        most_similar = 0
        most_similar_idx = 0
        for idx, result in enumerate(results):
            result_a = cast(Tag, result.find("a"))
            result_name = cast(NavigableString, result_a.string)

            similarity = SequenceMatcher(None, result_name, game).ratio()
            if similarity > most_similar:
                most_similar = similarity
                most_similar_idx = idx

        return results[most_similar_idx]

    def __get_compat_data(self, rows: ResultSet[Tag]) -> list[dict[str, str]]:
        """Get compatibility data for each method listed for the game"""
        compat_data: list[dict[str, str]] = []

        for row in rows:
            row_data = {"method": "", "rating": ""}

            # Method (e.x. Native, Rosetta 2, CrossOver, Parallels, etc.)
            method_th = cast(
                Tag, row.find("th", {"class": "table-compatibility-body-method"})
            )
            method_a = method_th.find("a")

            if type(method_a) is Tag:
                method = cast(NavigableString, method_a.string)
            else:
                method = cast(NavigableString, method_th.string)

            row_data["method"] = method

            # Rating (e.x. Perfect, Playable, Unplayable, Unknown, etc.)
            rating_td = cast(
                Tag, row.find("td", {"class": "table-compatibility-body-rating"})
            )
            rating_span = cast(Tag, rating_td.find("span"))
            rating = cast(NavigableString, rating_span.string)

            row_data["rating"] = rating

            compat_data.append(row_data)

        return compat_data

    def __build_embed(
        self, title: str, data: list[dict[str, str]], url: str, ctx: lb.Context
    ) -> hk.Embed:
        """Create the response embed showing the collected info"""
        embed = hk.Embed(title=title, colour=ctx.user.accent_colour)

        _ = embed.set_footer(
            "via applegamingwiki.com",
            icon="https://static.pcgamingwiki.com/favicons/applegamingwiki.png",
        )

        for method in data:
            _ = embed.add_field(
                name=method["method"], value=method["rating"], inline=True
            )

        _ = embed.add_field(
            value=f"[**Link ↗**]({url})",
            inline=False,
        )

        return embed

    async def __resp_no_game(self, game: str, ctx: lb.Context):
        """Respond to the user in the event that the game is not found"""
        _ = await ctx.respond(
            f"Sorry, I couldn't find '{game}' on [**AppleGamingWiki**](<https://www.applegamingwiki.com/>). Please check your spelling and try again",
            ephemeral=True,
        )


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
        # Get game search page data
        game_search = "+".join(self.game.split(" "))
        search_url = f"https://www.codeweavers.com/compatibility?browse=&app_desc=&company=&rating=&platform=&date_start=&date_end=&name={game_search}&search=app#results"
        search_page_soup = self.__get_page(search_url)

        # Get list of game links
        app_list = search_page_soup.find(id="teTable-app")
        if type(app_list) is Tag:
            apps = cast(ResultSet[Tag], app_list.find_all("a"))
        else:
            _ = await self.__resp_no_game(self.game, ctx)
            return

        # Get info for most similar search result
        game_tag = self.__find_most_similar(self.game, apps)
        db_name = game_tag.string
        rel_link = game_tag["href"]

        # Get game page data
        game_url = f"https://www.codeweavers.com/{rel_link}"
        game_soup = self.__get_page(game_url)

        # Find current star rating
        all_star_tables = game_soup.find_all("ul", {"class": "star-rating-table"})
        star_table: Tag = cast(Tag, all_star_tables[0])

        # Get game performance rating and description
        rating = self.__get_rating(star_table)
        rating_desc = self.__get_rating_desc(rating)

        _ = await ctx.respond(
            "",
            embed=self.__build_embed(db_name, rating, rating_desc, game_url, ctx),
        )

    def __get_page(self, url: str) -> bs:
        """Return parsed page data for the given URL"""
        page = requests.get(url)
        return bs(page.content, "html.parser")

    def __find_most_similar(self, game: str, apps: ResultSet[Tag]) -> Tag:
        """Find the search result with the most similar name to the user's search"""
        most_similar = 0
        most_similar_idx = 0
        for idx, app in enumerate(apps):
            assert type(app.string) is NavigableString

            similarity = SequenceMatcher(None, app.string, game).ratio()
            if similarity > most_similar:
                most_similar = similarity
                most_similar_idx = idx

        return apps[most_similar_idx]

    def __get_rating(self, star_table: Tag) -> int:
        """Read how many active stars are in the game's rating"""
        rating = 0

        for star in star_table:
            assert type(star) is Tag

            try:
                if star["class"] == ["active"]:
                    rating += 1
            except KeyError:
                break

        return rating

    def __get_rating_desc(self, rating: int) -> str:
        """Get the rating description matching the game's star rating"""
        match rating:
            case 1:
                return "Will Not Install"
            case 2:
                return "Installs, Will Not Run"
            case 3:
                return "Limited Functionality"
            case 4:
                return "Runs Well"
            case 5:
                return "Runs Great"
            case _:
                return "Unknown"

    def __build_embed(
        self, title: str | None, stars: int, desc: str, game_url: str, ctx: lb.Context
    ) -> hk.Embed:
        """Create the response embed showing collected info"""
        embed = hk.Embed(
            title=title,
            colour=ctx.user.accent_colour,
        )

        _ = embed.set_footer(
            "via codeweavers.com",
            icon="https://media.codeweavers.com/pub/crossover/website/images/cw_logo_128.png",
        )

        _ = embed.add_field(
            name="Rating",
            value=f"{':star:' * stars} ({desc})",
            inline=False,
        )

        _ = embed.add_field(
            value=f"[**Link ↗**]({game_url})",
            inline=False,
        )

        return embed

    async def __resp_no_game(self, game: str, ctx: lb.Context):
        """Respond to the user in the event that the game is not found"""
        _ = await ctx.respond(
            f"Sorry, I couldn't find '{game}' in the [**CrossOver Compatibility Database**](<https://www.codeweavers.com/compatibility>). Please check your spelling and try again",
            ephemeral=True,
        )


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
                ephemeral=True,
            )
