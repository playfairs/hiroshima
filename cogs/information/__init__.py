from .information import Information
from main import Hiroshima

async def setup(bot: Hiroshima):
    await bot.add_cog(Information(bot, Hiroshima))