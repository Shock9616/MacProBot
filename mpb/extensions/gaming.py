#
# gaming.py
#
# The gaming extension for MacProBot. Contains commands related to Mac gaming
#

from difflib import SequenceMatcher
import datetime as dt

import hikari as hk
import lightbulb as lb
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Tag, ResultSet

loader = lb.Loader()


@loader.command
class CxRating(
    lb.SlashCommand,
    name="cx_rating",
    description="Checks if the bot is alive",
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
                f"Sorry, I couldn't find {self.game} in the CrossOver Compatibility Database."
            )
            return

        # Find app with most similar name
        most_similar = 0
        most_similar_idx = 0
        idx = 0
        for app in apps:
            if type(app.string) is str:
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
        star_table: Tag = soup.find_all("ul", class_="star-rating-table")[0]

        # Count stars
        star_count = 0
        for star in star_table:
            if type(star) is Tag:
                try:
                    if star["class"] == ["active"]:
                        star_count += 1
                except KeyError:
                    break

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
            name="Page Link",
            value=game_page_url,
            inline=False,
        )

        _ = await ctx.respond("", embed=embed)
