import time
import asyncio
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
            await asyncio.sleep(20)
            if member in member.guild.members:  # If member isn't a bot (95% accurate)
                channel = member.guild.get_channel(1066357407443333190)
                embed = discord.Embed(color=utils.Colors.purple)
                embed.set_thumbnail(url=member.display_avatar)
                embed.description = f"""
Welcome to the server, {member.mention}!\nFeel free to visit <id:customize> for roles & channels and <id:guide> for some useful info!
__**IMPORTANT**__: To gain access to the rest of the server,you need to first gain a level by chatting in this channel.
Thank you for reading and have fun!"""
                await channel.send(content=f"<@&822886791312703518>, welcome {member.mention}", embed=embed)
                await self.inactives_checker.addMember((member.id, time.time()))

    @commands.Cog.listener()
    async def on_member_update(self, member, member_new: discord.Member):
        if member_new.guild.id == 715969701771083817:
            if not member_new in member_new.guild.members:
                return
            botroles_list = [891021633505071174, 731233454716354710]  # Red, Bear
            botroles_list2 = [891021633505071174, 731233454716354710, 731245341495787541,
                              731241481284616282, 731241703100383242, 738350937659408484, 738356235841175594]  # Red, Bear Hetero, Male, Single, Europe, Chat Revival
            ignored_roles = [1165755854730035301,  # Unverified role
                             715969701771083817,  # Everyone
                             778893728701087744]  # Townsfolk
            member_roles = [role.id for role in member_new.roles if role.id not in ignored_roles]
            old_member_roles = [role.id for role in member.roles if role.id not in ignored_roles]
            member_roles_match = set(member_roles) == set(botroles_list) or set(member_roles) == set(botroles_list2)  # boolean for both role checks on the new member
            old_member_roles_match = set(old_member_roles) == set(botroles_list) or set(old_member_roles) == set(botroles_list2)  # boolean for both role checks on the old member
            if member_roles_match or old_member_roles_match or len(member_new.roles) == 78:
                try:
                    await member_new.send("You've been kicked from The Paw Kingdom for botlike behaviour. If you are a human, rejoin and select different selfroles")
                except Exception:
                    pass
                try:
                    await member_new.kick(reason="Bot")
                except Exception as e:
                    print(f"Unable to kick bot {member_new.display_name} ({member_new.id}). Error:\n{e}")
                    return
                channel = member_new.guild.get_channel(1066357407443333190)
                logchannel = member_new.guild.get_channel(760181839033139260)
                embed = discord.Embed(color=utils.Colors.orange)
                embed.set_author(name=f"Bot Kick | {member_new.display_name}", icon_url=member_new.display_avatar.url)
                embed.set_footer(text=member_new.id)
                embed.description = f"**User**: {member_new.mention}\n**User ID**: {member_new.id}"
                await logchannel.send(embed=embed)
                async for message in channel.history(limit=15):
                    if member_new in message.mentions:
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
