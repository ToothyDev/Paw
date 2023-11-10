import time
from discord.ext import commands
import discord
from discord import SlashCommandGroup
import utils


class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot
        self.inactives_checker = utils.AutoVerify(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 715969701771083817:
            await self.inactives_checker.addMember((member.id, time.time()))

    @commands.Cog.listener()
    async def on_member_update(self, member, member_new):
        if member_new.guild.id == 715969701771083817:
            botroles_list = [715969701771083817, 778893728701087744, 891021633505071174, 731233454716354710]  # Everyone, townsfolk, red, bear
            botroles_list2 = [715969701771083817, 778893728701087744, 891021633505071174, 731233454716354710,
                              731245341495787541, 731241481284616282, 731241703100383242, 738350937659408484,
                              738356235841175594]  # Above plus hetero, male, single, europe, chat revival
            ignored_role = 1165755854730035301  # Unverified role
            member_roles = [role.id for role in member_new.roles if role.id != ignored_role]
            if set(member_roles) == set(botroles_list) or set(member_roles) == set(botroles_list2):
                try:
                    await member.send("You've been kicked from The Paw Kingdom for botlike behaviour. If you are a human, rejoin and select different selfroles")
                except Exception:
                    pass
                await member.kick(reason="Bot")
                channel = member_new.guild.get_channel(1066357407443333190)
                await channel.purge(limit=1, reason="Deleting bot join message")
                return
            await utils.unverified(member_new.guild)

    inactives = SlashCommandGroup(name="inactives", default_member_permissions=discord.Permissions(manage_guild=True, kick_members=True))

    @inactives.command()
    @discord.default_permissions()
    async def get(self, ctx):
        """ Get all inactive members """
        await ctx.defer()
        members = await self.inactives_checker.getMembers()
        await ctx.respond(members)


def setup(bot):
    bot.add_cog(Members(bot))
