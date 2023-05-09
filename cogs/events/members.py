import discord
import config
from discord.ext import commands


# from cogs.admin import admin_only

class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Members(bot))
