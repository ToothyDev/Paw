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
    async def on_member_update(self, member, member_new: discord.Member):
        if member_new.guild.id == 715969701771083817:
            botroles_list = [891021633505071174, 731233454716354710]  # Red, Bear
            botroles_list2 = [891021633505071174, 731233454716354710, 731245341495787541,
                              731241481284616282, 731241703100383242, 738350937659408484, 738356235841175594]  # Red, Bear Hetero, Male, Single, Europe, Chat Revival
            ignored_roles = [1165755854730035301,  # Unverified role
                             715969701771083817,  # Everyone
                             778893728701087744]  # Townsfolk
            member_roles = [role.id for role in member_new.roles if role.id not in ignored_roles]
            if set(member_roles) == set(botroles_list) or set(member_roles) == set(botroles_list2):
                try:
                    await member.send("You've been kicked from The Paw Kingdom for botlike behaviour. If you are a human, rejoin and select different selfroles")
                except Exception:
                    pass
                try:
                    await member.kick(reason="Bot")
                except Exception as e:
                    print(f"Unable to kick bot {member.display_name} ({member.id}). Error:\n{e}")
                    return
                channel = member_new.guild.get_channel(1066357407443333190)
                logchannel = member_new.guild.get_channel(760181839033139260)
                embed = discord.Embed(color=utils.Colors.orange)
                embed.set_author(name=f"Bot Kick | {member_new.display_name}", icon_url=member_new.avatar.url)
                embed.set_footer(text=member_new.id)
                embed.description = f"**User**: {member_new.mention}\n**User ID**: {member_new.id}"
                await logchannel.send(embed=embed)
                embed = discord.Embed(color=utils.Colors.orange)
                embed.set_author(name=f"Bot Kick | {member_new.display_name}", icon_url=member_new.avatar.url)
                embed.set_footer(text=member_new.id)
                embed.description = f"**User**: {member_new.mention}\n**User ID**: {member_new.id}"
                await logchannel.send(embed=embed)
                async for message in channel.history(limit=15):
                    if member in message.content.mentions:
                        await message.delete(reason="Deleting bot join message")
                        break
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
