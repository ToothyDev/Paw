import gifs
from discord.ext import commands
import random
import discord

class assets(commands.Cog, name="assets"):
    def __init__(self, bot):
        self.bot = bot

@commands.command(brief="Art of Paw")
async def paw(ctx):
    embed = discord.Embed(title="A picture of myself, Paw!",color=discord.Color.blue())
    embed.set_image(url=random.choice(gifs.paw))
    return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(assets(bot))
    