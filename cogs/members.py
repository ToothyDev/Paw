from discord.ext import commands
import utils
import time
import discord
from discord import SlashCommandGroup


class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot
        self.inactives_checker = utils.AutoVerify(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 715969701771083817:
            self.inactives_checker.addMember((member.id, time.time()))

    inactives = SlashCommandGroup(name="inactives", default_member_permissions=discord.Permissions(manage_guild=True, kick_members=True))

    @inactives.command()
    @discord.default_permissions(manage_guild=True)
    async def get(self, ctx):
        """ Get all inactive members """
        await ctx.respond(await self.inactives_checker.getMembers())


def setup(bot):
    bot.add_cog(Members(bot))
