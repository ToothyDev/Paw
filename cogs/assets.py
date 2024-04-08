import random

import discord
from discord import slash_command

import data
from utils import Colors


class Assets(discord.Cog, name="assets"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def paw(self, ctx):
        """ Get random art of me, Paw """
        embed = discord.Embed(title="A picture of myself, Paw!", color=Colors.blue)
        embed.set_image(url=random.choice(data.paw))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Assets(bot))
