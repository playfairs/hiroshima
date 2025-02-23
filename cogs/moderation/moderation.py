import discord
import aiohttp
import asyncio
import io
import os
import json
import traceback
from datetime import datetime, timedelta
from typing import Optional, Union

from discord.ext import commands, tasks
from discord.ext.commands import command, group, has_permissions, Context, Cog
from discord.ui import Button, View
from discord import Member
from discord.app_commands import command as acommand
from discord import AutoModRuleEventType, AutoModRuleTriggerType, AutoModRuleAction, AutoModAction
from buttons import BUTTON

class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession()
        self.sniped_messages = {}
        self.edited_messages = {}
        self.snipe_reset.start()
        self.sniped_reactions = {}
        self.user_owner = self.bot.get_user(785042666475225109)

    @tasks.loop(minutes=60)
    async def snipe_reset(self):
        self.sniped_messages.clear()
        self.edited_messages.clear()
        self.sniped_reactions.clear()

    @Cog.listener()
    async def on_ready(self):
        if not self.snipe_reset.is_running:
            self.snipe_reset.start()

    @command(name="ban", description="Bans the specified member with a specified reason.")
    @has_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: Optional[Member] = None, *, reason: str = "No reason provided.") -> None:
        if member is None:
            await ctx.send("You must specify a user to ban")
        if member.id == self.user_owner.id:
            await ctx.send("no")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"👍")
        except Exception as e:
            await ctx.send(f"sum shit went wrong:{str(e)}")


    @command(name="unban", description="Unbans the specified member with a specified reason.")
    @has_permissions(ban_members=True)
    async def unban(self, ctx: Context, member: Optional[Member] = None, *, reason: str = "No reason provided.") -> None:
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send("I do not have permission to unban members.")
        if member is None:
            await ctx.send("You must specify a user to unban")
            return
        try:
            await member.unban(reason=reason)
            await ctx.send(f"👍")
        except Exception as e:
            await ctx.send(f"sum shit went wrong:{str(e)}")

    @command(name="kick", description="Kicks the specified member with a specified reason.")
    @has_permissions(kick_members=True)
    async def kick (self, ctx: Context, member: Member, *, reason: str = "No reason provided.") -> None:
        if member.id == self.user_owner.id:
            await ctx.send("no")
            return
        try:
            await member.kick(reason=reason)
            await ctx.send(f"👍")
        except Exception as e:
            await ctx.send(f"sum shit went wrong:{str(e)}")

    @command(name="mute", description="Mutes the specified member with a specified reason.")
    @has_permissions(moderate_members=True)
    async def mute(self, ctx: Context, member: Member, *, reason: str = "No reason provided.") -> None:
        if not ctx.guild.me.guild_permissions.mute_members:
            await ctx.send("I do not have permission to mute members.")
        if member.id == self.user_owner.id:
            await ctx.send("no")
            return
        try:
            await member.mute(reason=reason)
            await ctx.send(f"👍")
        except Exception as e:
            await ctx.send(f"sum shit went wrong:{str(e)}")

    @command(name="unmute", description="Unmutes the specified member with a specified reason.")
    @has_permissions(moderate_members=True)
    async def unmute(self, ctx: Context, member: Member, *, reason: str = "No reason provided.") -> None:
        if not ctx.guild.me.guild_permissions.mute_members:
            await ctx.send("I do not have permission to unmute members.")
        if member.id == self.user_owner.id:
            await ctx.send("no")
            return
        try:
            await member.unmute(reason=reason)
            await ctx.send(f"👍")
        except Exception as e:
            await ctx.send(f"sum shit went wrong:{str(e)}")

    @command(name="softban", description="Softbans the specified member with a specified reason.")
    @has_permissions(ban_members=True)
    async def softban(self, ctx: Context, member: Member, *, reason: str = "No reason provided.") -> None:
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send("I do not have permission to softban members.")
        if member.id == self.user_owner.id:
            await ctx.send("no")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"👍")
        except Exception as e:
            await ctx.send(f"sum shit went wrong:{str(e)}")

    @command(name="nuke", aliases=['arab', 'twintowers', 'hiroshima', 'nagasaki', 'japan1945', 'ww2', 'boomboom'])
    @has_permissions(administrator=True)
    async def nuke(self, ctx):
        """Nukes the current channel with confirmation."""
        class ConfirmView(discord.ui.View):
            def __init__(self, ctx, original_channel):
                super().__init__()
                self.ctx = ctx
                self.original_channel = original_channel
                self.button_messages = BUTTON()

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != self.ctx.author:
                    await interaction.response.send_message("Don't touch my button.. it turns me on..", ephemeral=True)
                    return

                category = self.original_channel.category
                position = self.original_channel.position
                topic = self.original_channel.topic
                nsfw = self.original_channel.is_nsfw()
                overwrites = self.original_channel.overwrites

                await self.original_channel.delete()

                new_channel = await self.ctx.guild.create_text_channel(
                    name=self.original_channel.name,
                    category=category,
                    position=position,
                    topic=topic,
                    nsfw=nsfw,
                    overwrites=overwrites
                )

                embed = discord.Embed(
                    title="Channel Nuked", 
                    description=f"This channel was nuked by {self.ctx.author.mention}",
                    color=discord.Color.red()
                )
                await new_channel.send(embed=embed)


            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
            async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != self.ctx.author:
                    await interaction.response.send_message("Don't touch my button.. it turns me on..", ephemeral=True)
                    return

                await interaction.response.send_message("Cancelled", ephemeral=True)
                await interaction.message.delete()

        embed = discord.Embed(
            title="Nuke Confirmation", 
            description="Are you sure you want to nuke this channel? This will delete and recreate the channel.",
            color=discord.Color.red()
        )
        
        view = ConfirmView(ctx, ctx.channel)
        await ctx.send(embed=embed, view=view)
