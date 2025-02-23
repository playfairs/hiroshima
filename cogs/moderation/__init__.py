from .moderation import Moderation
from discord.ext.commands import Cog

async def setup(bot):
    await bot.add_cog(Moderation(bot))
