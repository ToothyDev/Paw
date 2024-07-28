import discord

from discord.ext import tasks

import utils


class Members(discord.Cog, name="Members"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.auto_kicker.start()

    inactives = discord.SlashCommandGroup(name="inactives",
                                          default_member_permissions=discord.Permissions(manage_guild=True,
                                                                                         kick_members=True))

    @tasks.loop(hours=6)
    async def auto_kicker(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(715969701771083817)
        to_be_kicked = await utils.InactivesTracker.get_raw_members(guild)
        for member in to_be_kicked:
            try:
                await member.send(
                    "You've been kicked from The Paw Kingdom for being inactive for too long. You can rejoin and restart the verification process.")
            except Exception or discord.Forbidden:
                pass
            try:
                #  await member.kick(reason="Inactive Member")
                await self.bot.get_channel(759760673738719252).send(f"I'd kick {member.mention}!")
            except discord.Forbidden:
                print(f"Failed to kick member {member.global_name}!")
        await self.bot.get_channel(759760673738719252).send("Autokicker task is running")

    @inactives.command()
    async def get(self, ctx: discord.ApplicationContext):
        """ Get all inactive members """
        members = await utils.InactivesTracker.get_members(ctx.guild)
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
