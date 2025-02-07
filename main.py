import asyncpg
import logging

from pathlib import Path
from discord.ext import commands
from discord import Intents, AllowedMentions
# from core.client import HelpNavigator

from config import DISCORD

log = logging.getLogger(__name__)

if not log.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.INFO)

class Hiroshima(commands.AutoShardedBot):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            command_prefix=DISCORD.PREFIX,
            help_command=None,
            shard_count=2,
            intents=Intents(
                guilds=True,
                members=True,
                messages=True,
                reactions=True,
                presences=True,
                moderation=True,
                message_content=True,
                emojis_and_stickers=True,
                typing=True
            ),
            allowed_mentions=AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=True
            ),
        )
        self.owner_ids = DISCORD.OWNER_IDS

    def run(self) -> None:
        log.info("Starting Hiroshima.")

        super().run(
            DISCORD.TOKEN,
            reconnect=True,
            # log_handler=log
        )

    async def load_extensions(self) -> None:
        await self.load_extension("jishaku")
        for feature in Path("cogs").iterdir():
            if feature.is_dir() and (feature / "__init__.py").is_file():
                try:
                    cog_name = ".".join(feature.parts)
                    print(f"Loading cog: {cog_name}")
                    await self.load_extension(cog_name)
                    print(f"Successfully loaded: {cog_name}")
                except Exception as exc:
                    log.exception(
                        f"Failed to load extension {feature.name}", exc_info=exc
                    )
    # async def create_db_pool(self):
        # self.db_pool = await asyncpg.create_pool(
            # port="5433",
            # database="hiroshima",
            # user="postgress",
            # host="localhost",
            # password="admin"
        # )

    async def setup_hook(self):
        # await self.create_db_pool()
        await self.load_extensions()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Shard ID: {self.shard_id} of {self.shard_count} shards')
        print(f'Guilds: {len(self.guilds)}')
        print(f'Hiroshima v1.0.0')

        for guild in self.guilds:
            try:
                await self.tree.sync(guild=guild)
                print(f"Synced commands for guild {guild.name}")
            except Exception as e:
                print(f"Failed to sync commands for guild {guild.name}: {e}")

        print("Bot is ready and connected.")


    async def get_prefix(self, message):
        prefixes = ['?', '!']
        return commands.when_mentioned_or(*prefixes)(self, message)

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        
        if ctx.command is not None:
            ctx.invoked_with = ctx.invoked_with.lower()

            if ctx.command.name == 'help' in ctx.command.aliases:
                if len(ctx.args) > 2:
                    ctx.args = list(ctx.args)
                    ctx.args[2] = ctx.args[2].lower()
        
        await self.invoke(ctx)

    async def invoke(self, ctx):
        if ctx.command is not None:
            ctx.command.name = ctx.command.name.lower()
            if hasattr(ctx.command, 'aliases'):
                ctx.command.aliases = [alias.lower() for alias in ctx.command.aliases]

        await super().invoke(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction('❓')

if __name__ == "__main__":
    bot = Hiroshima()
    bot.run()
