from discord.ext import commands
import utils
import time
import discord
from discord import slash_command


class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot
        self.memberkicker = utils.AutoVerify(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 715969701771083817:
            self.memberkicker.addMember((member.id, time.time()))

    @slash_command()
    @discord.default_permissions(manage_guild=True)
    async def getinactive(self, ctx):
        await ctx.respond(self.memberkicker.getMembers())


def setup(bot):
    bot.add_cog(Members(bot))
