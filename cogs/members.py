from discord.ext import commands
import utils
import time
import discord
from discord import SlashCommandGroup
from cogs.utility import ConfirmView


class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot
        self.memberkicker = utils.AutoVerify(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 715969701771083817:
            self.memberkicker.addMember((member.id, time.time()))

    inactives = SlashCommandGroup(name="inactives", default_member_permissions=discord.Permissions(manage_guild=True, kick_members=True))

    @inactives.command()
    @discord.default_permissions(manage_guild=True)
    async def get(self, ctx):
        """ Get all inactive members """
        await ctx.respond(self.memberkicker.getMembers())

    @inactives.command()
    @discord.default_permissions(manage_guild=True)
    async def kick(self, ctx):
        """ Kick all inactive members """
        view = ConfirmView()
        await ctx.respond("Are you sure?", view=view)
        await view.wait()
        if not view.confirmed:
            return
        await ctx.respond(f"Kicked {await self.memberkicker.kickMembers()} members!")


def setup(bot):
    bot.add_cog(Members(bot))
