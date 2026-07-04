#
# deals.py
#
# Commands/functionality related to fetching deal info for users
#

import dotenv
import hikari as hk
import lightbulb as lb
import requests

_ = dotenv.load_dotenv()

loader = lb.Loader()


@loader.command
class Deals(
    lb.SlashCommand,
    name="deals",
    description="Get a list of currently available deals on Steam",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        resp = requests.get(
            "https://store.steampowered.com/api/featuredcategories",
            params={"cc": "us", "l": "en"},
        )
        data = resp.json()

        embeds: list[hk.Embed] = []

        for game in data["specials"]["items"][:5]:
            name = game["name"]
            thumbnail = game["small_capsule_image"]
            price = game["final_price"] / 100
            discount = game["discount_percent"]
            id = game["id"]
            mac = game["mac_available"]

            embeds.append(self.__build_embed(name, thumbnail, price, discount, id, mac))

        # Link to more deals
        embed = hk.Embed(title="See more deals on Steam!")
        embed.add_field(
            value=self.__pad_text(
                "[**More Deals ↗**](https://store.steampowered.com/specials)",
                target=143,
            )
        )
        embeds.append(embed)

        await ctx.respond("", embeds=embeds, ephemeral=True)

    def __build_embed(
        self, name: str, thumbnail: str, price: float, discount: int, id: int, mac: bool
    ) -> hk.Embed:
        """Build an embed with the provided game info"""
        url = f"https://store.steampowered.com/app/{id}"

        embed = hk.Embed(title=name)
        embed.set_thumbnail(thumbnail)
        embed.add_field(value=f"**${price:.2f}** ({discount}% off)")
        embed.add_field(value=self.__pad_text(f"[**Store Page ↗**]({url})"))

        return embed

    def __pad_text(self, text: str, target: int = 116) -> str:
        """Pad the provided text to force the width of the embed to be consistent"""
        pad_char = " \u200b"
        if len(text) < target:
            text += pad_char * (target - len(text))

        return text
