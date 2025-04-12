#
# gaming.py
#
# The gaming extension for MacProBot. Contains commands related to Mac gaming
#

# pyright: reportIgnoreCommentWithoutRule=false

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
        # _ = await ctx.respond(
        #     f"Searching CrossOver Compatibility Database for {self.game}. Please wait..."
        # )

        game_search = "+".join(self.game.split(" "))
        search_url = f"https://www.codeweavers.com/compatibility?browse=&app_desc=&company=&rating=&platform=&date_start=&date_end=&name={game_search}&search=app#results"
        search_page = requests.get(search_url)
        search_page_soup = bs(search_page.content, "html.parser")
        rel_link = search_page_soup.find_all("a", string=self.game)[0]["href"]  # pyright:ignore

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

        _ = await ctx.respond(
            f"{self.game} currently has a rating of {star_count}/5 stars"
        )
