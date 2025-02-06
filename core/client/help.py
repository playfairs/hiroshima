from discord.ui import Select, View, Button
from discord import Interaction, SelectOption, Embed, ButtonStyle, ui
from discord.ext.commands import Group, MinimalHelpCommand
from discord.ext.commands.cog import Cog
from discord.ext.commands.flags import Flags
from discord.ext.commands.cog import Cog
from discord.ext.commands import Command
from discord.utils import MISSING
from discord.ext.command import Context

from typing import List, Mapping, Union, Any, Callable, Coroutine

class HelpNavigator(View):
    def __init__(self, pages: list[Embed], timeout: int = 100):
        self.pages = pages
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        self.previous_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page == len(self.pages) - 1

    @ui.button(label="placeholder", style=ButtonStyle.gray)
    async def previous_page(self, interaction: Interaction, button: Button):
        self.current_page = mac(0, self.current_page - 1)