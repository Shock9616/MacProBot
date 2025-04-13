#
# gaming.py
#
# The gaming extension for MacProBot. Contains commands related to Mac gaming
#

# pyright: reportIgnoreCommentWithoutRule=false

from difflib import SequenceMatcher
import datetime as dt

import hikari as hk
import lightbulb as lb
import requests
from bs4 import BeautifulSoup as bs

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
        if app_list is not None:
            apps = app_list.find_all("a")  # pyright:ignore
        else:
            _ = await ctx.respond(
                f"Sorry, I couldn't find {self.game} in the CrossOver Compatibility Database."
            )
            return

        # Find app with most similar name
        most_similar = 0
        most_similar_idx = 0
        idx = 0
        for app in apps:  # pyright:ignore
            similarity = SequenceMatcher(app.string, self.game).ratio()  # pyright:ignore
            if similarity > most_similar:
                most_similar = similarity
                most_similar_idx = idx
            idx += 1

        db_name = apps[most_similar_idx].string  # pyright:ignore
        rel_link = apps[most_similar_idx]["href"]  # pyright:ignore

        # Get page data
        game_page_url = f"https://www.codeweavers.com/{rel_link}"
        game_page = requests.get(game_page_url)
        soup = bs(game_page.content, "html.parser")

        # Find current star rating
        star_table = soup.find_all("ul", class_="star-rating-table")[0]

        # Count stars
        star_count = 0
        for star in star_table:  # pyright:ignore
            try:
                if star["class"] == ["active"]:
                    star_count += 1
            except KeyError:
                pass

        rating_desc = "Unkown"
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
                pass

        embed = hk.Embed(
            title=db_name,  # pyright:ignore
            colour=ctx.user.accent_colour,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )

        embed.set_footer(  # pyright:ignore
            text=f"Requested by {ctx.user.username}", icon=ctx.user.avatar_url
        )

        embed.add_field(  # pyright:ignore
            name="Rating",
            value=f"{':star:' * star_count} ({rating_desc})",
            inline=False,
        )

        _ = await ctx.respond("", embed=embed)
