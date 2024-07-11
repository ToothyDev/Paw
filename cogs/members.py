import asyncio
import time

import discord

import utils


class Members(discord.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def send_welcome_message(member: discord.Member):
        channel = member.guild.get_channel(1066357407443333190)
        embed = discord.Embed(color=utils.Colors.purple)
        embed.set_thumbnail(url=member.display_avatar)
        embed.description = f"""
Welcome to the server, {member.mention}!\nFeel free to visit <id:customize> for roles & channels and <id:guide> for some useful info!
__**IMPORTANT**__: To gain access to the rest of the server, you need to first gain a level by chatting in this channel.
Thank you for reading and have fun!"""
        await channel.send(content=f"<@&822886791312703518>, welcome {member.mention}", embed=embed)

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.guild.id == 715969701771083817:
            return
        if member.bot:  # If member is an ACTUAL bot
            return

        await utils.InactivesTracker.add_member((member.id, time.time()))

    @discord.Cog.listener()
    async def on_member_update(self, member_old: discord.Member, member: discord.Member):
        if not member.guild.id == 715969701771083817:
            return

        if member.bot:  # If member is an ACTUAL bot
            return

        if await utils.userbot_kicker(member):  # If member is a bot (95% accurate)
            return

        await utils.unverified_role_handler(member.guild)

        if len(member_old.roles) <= 2 < len(member.roles):
            if member.pending:
                return
            await self.send_welcome_message(member)
        elif len(member.roles) >= 3:
            if member_old.pending and not member.pending:
                await self.send_welcome_message(member)

    inactives = discord.SlashCommandGroup(name="inactives",
                                          default_member_permissions=discord.Permissions(manage_guild=True,
                                                                                         kick_members=True))

    @inactives.command()
    async def get(self, ctx):
        """ Get all inactive members """
        await ctx.defer()
        members = await utils.InactivesTracker.get_members(self.bot)
        await ctx.respond(members)

    @inactives.command()
    async def pending(self, ctx):
        """ Get all non-verified accounts (unsure what that means) """
        output = ""
        for member in ctx.guild.members:
            if member.pending:
                output += " " + member.mention
        if not output:
            output = "No members found!"
        await ctx.respond(output)


def setup(bot):
    bot.add_cog(Members(bot))
