from .utility import Utility
from main import Hiroshima

async def setup(bot: Hiroshima):
    await bot.add_cog(Utility(bot))