import discord
import os

from discord.ext import commands
from discord.ext.commands import Cog, command, Context
from deep_translator import GoogleTranslator
from main import Hiroshima

class Utility(Cog):
    def __init__(self, bot):
        self.bot = bot

# Add commands later