from .owner import Owner
from main import Hiroshima

async def setup(bot: Hiroshima):
    await bot.add_cog(Owner(bot))