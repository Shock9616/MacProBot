#
# help.py
#
# Separate extension for the help command
#

import asyncio

import hikari as hk
import lightbulb as lb
from lightbulb.components import InteractiveButton

loader = lb.Loader()


class HelpMenu(lb.components.Menu):
    def __init__(self, command_metadata: list[dict[str, str]]):
        super().__init__()

        self.current_page_id: int = 0

        self.page_list: list[hk.Embed] = []
        self.total_pages: int = int(len(command_metadata) / 5) + (
            1 if len(command_metadata) % 5 != 0 else 0
        )

        for i in range(self.total_pages):
            page = hk.Embed(title="MacProBot Help")

            for j in range(5):
                try:
                    _ = page.add_field(
                        name=f"`{command_metadata[i * 5 + j]['title']}`",
                        value=command_metadata[i * 5 + j]["desc"],
                        inline=False,
                    )
                except IndexError:
                    break

            _ = page.set_footer(text=f"Page {i + 1} of {self.total_pages}")
            self.page_list.append(page)

        self.first_button: InteractiveButton = self.add_interactive_button(
            hk.ButtonStyle.PRIMARY, self.on_first_button_pressed, label="⏮"
        )
        self.prev_button: InteractiveButton = self.add_interactive_button(
            hk.ButtonStyle.SECONDARY, self.on_prev_button_pressed, label="⏴"
        )
        self.next_button: InteractiveButton = self.add_interactive_button(
            hk.ButtonStyle.SECONDARY, self.on_next_button_pressed, label="⏵"
        )
        self.last_button: InteractiveButton = self.add_interactive_button(
            hk.ButtonStyle.PRIMARY, self.on_last_button_pressed, label="⏭"
        )

    async def on_first_button_pressed(self, ctx: lb.components.MenuContext):
        self.current_page_id = 0

        _ = await ctx.respond(
            "",
            embed=self.page_list[self.current_page_id],
            edit=True,
            components=self,
        )

    async def on_prev_button_pressed(self, ctx: lb.components.MenuContext):
        if self.current_page_id > 0:
            self.current_page_id -= 1

        _ = await ctx.respond(
            "",
            embed=self.page_list[self.current_page_id],
            edit=True,
            components=self,
        )

    async def on_next_button_pressed(self, ctx: lb.components.MenuContext):
        if self.current_page_id < self.total_pages - 1:
            self.current_page_id += 1

        _ = await ctx.respond(
            "",
            embed=self.page_list[self.current_page_id],
            edit=True,
            components=self,
        )

    async def on_last_button_pressed(self, ctx: lb.components.MenuContext):
        self.current_page_id = self.total_pages - 1

        _ = await ctx.respond(
            "",
            embed=self.page_list[self.current_page_id],
            edit=True,
            components=self,
        )


@loader.command
class Help(
    lb.SlashCommand,
    name="help",
    description="Show help info and commands",
):
    @lb.invoke
    async def invoke(self, ctx: lb.Context):
        help_menu_items: list[dict[str, str]] = []

        # Generate list of available commands/descriptions
        for command in ctx.client.registered_commands:
            # Exclude mod-only commands and the help command
            if (
                command.__module__ != "mpb.extensions.admin"
                and command.__module__ != "mpb.extensions.help"
            ):
                help_menu_items.append(
                    {
                        "title": f"/{command._command_data.name}",
                        "desc": command._command_data.description,
                    }
                )

        help_menu = HelpMenu(sorted(help_menu_items, key=lambda d: d["title"]))

        _ = await ctx.respond(
            "",
            embed=help_menu.page_list[0],
            components=help_menu,
            ephemeral=True,
        )

        try:
            _ = await help_menu.attach(ctx.client, wait=True, timeout=30)
        except asyncio.TimeoutError:
            pass
