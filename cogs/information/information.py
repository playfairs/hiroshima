import discord
from discord.ext import commands
from discord.ext.commands import Cog, command, Context
import difflib
import asyncio
import platform
import os
import psutil
import subprocess

from datetime import datetime, timezone
from discord import Embed, Color
from discord import app_commands
from main import Hiroshima

class Information(Cog):
    def __init__(self, bot, Hiroshima):
        self.bot = bot
        self.developer_id = 785042666475225109
        self.bot_id = 1284037026672279635

    @app_commands.command(name="about", description="Displays information about either the Bot, or Playfair.")
    @app_commands.describe(target="Select either Hiroshima, or Playfair.")
    @app_commands.choices(
        target=[
            app_commands.Choice(name="Hiroshima", value="hiroshima"),
            app_commands.Choice(name="Playfair", value="playfair"),
        ]
    )
    async def about(self, interaction: discord.Interaction, target: app_commands.Choice[str]):
        option_value = target.value.lower()
        if option_value == "playfair":
            embed = discord.Embed(
                title="About Playfair",
                description="Developer of Heresy and Hiroshima",
                color=discord.Color.from_rgb(255, 255, 255)
            )
            embed.add_field(name="Description", value="Playfairs, or Playfair, is the developer of both Hiroshima, and Heresy.", inline=False)
            embed.add_field(name="Useful Links", value="[Website](https://playfairs.cc) | [GitHub](https://github.com/playfairs)", inline=False)
            embed.set_footer(text="Requested by: {}".format(interaction.user.name))

        elif option_value == "hiroshima":
            embed = discord.Embed(
                title="About Hiroshima",
                description="Hiroshima is a Antinuke and Moderation based bot meant to Secure and Protect your server. Developed and Maintained by <@785042666475225109>",
                color=discord.Color.from_rgb(255, 255, 255)
            )
            embed.add_field(name="Developer", value="<@785042666475225109>", inline=False)
            embed.add_field(name="Description", value="Discord.py", inline=False)
            embed.add_field(name="Useful Links", value="[Website](https://playfairs.cc/hiroshima) | [Repository](https://github.com/playfairs/hiroshima) | [Discord](https://discord.gg/heresy)", inline=False)
            embed.set_footer(text="For more information, DM @playfairs, or check ,help for more info.")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        """Displays basic information about the specified user or the interaction user if no member is specified."""
        member = member or interaction.user
        embed = discord.Embed(title=f"{member}'s Info", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Name", value=member.name, inline=False)
        embed.add_field(name="Created At", value=member.created_at.strftime("%m/%d/%Y, %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="banner", description="Show your banner.")
    async def banner(self, ctx, member: discord.Member = None):
        """Displays the banner of the specified user or yourself if no one is mentioned."""
        member = member or ctx.author
        user = await self.bot.fetch_user(member.id)

        if user.banner:
            embed = discord.Embed(title=f"{user.name}'s Banner", color=discord.Color.blue())
            embed.set_image(url=user.banner.url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} does not have a banner.")

    @commands.command(name="whois", aliases=['userinfo', 'ui', 'info', 'whoami'], help="Show detailed information about a user.")
    async def whois(self, ctx, member: discord.Member = None):
        """
        Displays detailed user information with badges, activity, and roles.
        """
        try:
            member = member or ctx.author
            if member.id == self.bot_id:
                await ctx.send("no")
                return
            developer_title = " - Developer" if member.id == self.developer_id else ""

            badges = []
            if member.public_flags.staff:
                badges.append("<:staff:1297931763229917246>")
            
            if member.public_flags.partner:
                badges.append("<:partner:1297931370357723198>")
            
            if member.public_flags.hypesquad:
                badges.append("<:hypesquad:1297930974633398293>")
            
            if member.public_flags.bug_hunter_level_2:
                badges.append("<:bug_hunter_level_2:1297931831521312850>")
            elif member.public_flags.bug_hunter:
                badges.append("<:bug_hunter:1297931813121036321>")
            
            if member.public_flags.early_supporter:
                badges.append("<:early_supporter:1297931252158042283>")
            
            if member.public_flags.verified_bot_developer:
                badges.append("<:verified_bot_developer:1297931270139150338>")
            
            if member.public_flags.discord_certified_moderator:
                badges.append("<:certified_moderator:1297932110514098290>")
            
            if member.public_flags.active_developer:
                badges.append("<:active_developer:1297930880987431035>")
            
            if member.public_flags.hypesquad_balance:
                badges.append("<:hypesquad_balance:1297930998864019509>")
            if member.public_flags.hypesquad_bravery:
                badges.append("<:hypesquad_bravery:1297931035421708358>")
            if member.public_flags.hypesquad_brilliance:
                badges.append("<:hypesquad_brilliance:1297931072503418890>")
            
            if member.premium_since:
                badges.append("<:boost:1297931223972450488>")
            
            if member == member.guild.owner:
                badges.append("<:server_owner:1297930836368167015>")
            
            if member.bot:
                badges.append("<a:bot2:1323899876924198976>")

            custom_emojis = " ".join(badges) if badges else "No badges"

            activities = member.activities
            listening = None
            playing = None

            for activity in activities:
                if isinstance(activity, discord.Spotify):
                    track_url = f"https://open.spotify.com/track/{activity.track_id}"
                    listening = f"[{activity.title} by {activity.artist}]({track_url})"
                elif isinstance(activity, discord.Game):
                    playing = f"{activity.name}"

            created_at = member.created_at.strftime("%B %d, %Y")
            joined_at = member.joined_at.strftime("%B %d, %Y")
            created_days_ago = (datetime.now(timezone.utc) - member.created_at).days
            joined_days_ago = (datetime.now(timezone.utc) - member.joined_at).days

            created_ago = f"{created_days_ago // 365} year{'s' if (created_days_ago // 365) > 1 else ''} ago" if created_days_ago >= 365 else f"{created_days_ago} day{'s' if created_days_ago > 1 else ''} ago"
            joined_ago = f"{joined_days_ago // 365} year{'s' if (joined_days_ago // 365) > 1 else ''} ago" if joined_days_ago >= 365 else f"{joined_days_ago} day{'s' if joined_days_ago > 1 else ''} ago"

            roles = sorted([role for role in member.roles[1:]], key=lambda x: x.position, reverse=True)
            top_roles = roles[:5]
            roles_string = " ".join(role.mention for role in top_roles) if top_roles else "No roles"
            if len(roles) > 5:
                roles_string += f" (+{len(roles) - 5} more)"

            if member.avatar:
                avatar_url = member.avatar.url
            else:
                avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url

            if ctx.author.avatar:
                footer_avatar_url = ctx.author.avatar.url
            else:
                footer_avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url

            embed = discord.Embed(color=discord.Color.dark_purple(), timestamp=datetime.utcnow())
            embed.set_author(name=f"{member.display_name}{developer_title}", icon_url=avatar_url)

            embed.set_thumbnail(url=avatar_url)

            embed.add_field(name="User ID", value=f"`{member.id}`", inline=False)

            embed.add_field(name="Badges", value=custom_emojis, inline=False)

            if listening:
                embed.add_field(name="Listening", value=listening, inline=False)
            if playing:
                embed.add_field(name="Playing", value=playing, inline=False)

            embed.add_field(name="Created", value=f"{created_at}\n{created_ago}", inline=True)
            embed.add_field(name="Joined", value=f"{joined_at}\n{joined_ago}", inline=True)

            embed.add_field(name="Roles", value=roles_string, inline=False)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=footer_avatar_url)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"**Error**: Something went wrong - {e}")
            raise e

    @commands.command(name="bi", aliases=['botinfo'], help="Shows detailed information about the bot.")
    async def show_bot_info(self, ctx):
        """Displays detailed information about the bot including stats and system info."""
        bot = self.bot
        
        total_members = sum(guild.member_count for guild in bot.guilds)
        total_guilds = len(bot.guilds)
        total_commands = len(bot.commands)
        total_cogs = len(bot.cogs)
        
        jishaku = self.bot.get_cog('Jishaku')
        if jishaku:
            uptime = datetime.now(timezone.utc) - jishaku.load_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        else:
            uptime_str = "Unable to calculate"

        total_lines = 0
        total_files = 0
        total_imports = 0
        total_functions = 0
        
        for root, _, files in os.walk("cogs"):
            for file in files:
                if file.endswith('.py'):
                    total_files += 1
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    total_lines += len(content.splitlines())
                    total_imports += len([line for line in content.splitlines() if line.strip().startswith(('import ', 'from '))])
                    total_functions += len([line for line in content.splitlines() if line.strip().startswith(('def ', 'async def '))])

        embed = discord.Embed(
            description=f"Developed and maintained by <@{self.developer_id}>\n`{total_commands}` commands | `{total_cogs}` cogs",
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="**Basic**",
            value=f"**Users**: `{total_members:,}`\n**Servers**: `{total_guilds:,}`\n**Created**: `{bot.user.created_at.strftime('%B %d, %Y')}`",
            inline=True
        )
        
        embed.add_field(
            name="**Runtime**",
            value=f"**OS**: `{platform.system()} {platform.release()}`\n**CPU**: `{psutil.cpu_percent()}%`\n**Memory**: `{psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB`\n**Uptime**: `{uptime_str}`",
            inline=True
        )
        
        embed.add_field(
            name="**Code**",
            value=f"**Files**: `{total_files}`\n**Lines**: `{total_lines:,}`\n**Functions**: `{total_functions}`\n**Library**: `discord.py {discord.__version__}`",
            inline=True
        )

        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        await ctx.send(embed=embed)