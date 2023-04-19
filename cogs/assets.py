import data
from discord.ext import commands, bridge
import random
import discord
from utils import Colors


class assets(commands.Cog, name="assets"):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(brief="Art of Paw")
    async def paw(self, ctx):
        embed = discord.Embed(title="A picture of myself, Paw!", color=Colors.blue)
        embed.set_image(url=random.choice(data.paw))
        return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(assets(bot))
