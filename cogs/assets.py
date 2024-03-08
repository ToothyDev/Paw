import random
import discord
from discord import slash_command
from discord.ext import commands
import data
from utils import Colors


class Assets(commands.Cog, name="assets"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(brief="Art of Paw")
    async def paw(self, ctx):
        """ Get random art of me, Paw """
        embed = discord.Embed(title="A picture of myself, Paw!", color=Colors.blue)
        embed.set_image(url=random.choice(data.paw))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Assets(bot))
