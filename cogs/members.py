import discord
from discord.ext import tasks

import logger
import utils

log = logger.get_logger(__name__)


class Members(discord.Cog, name="Members"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.auto_kicker.start()

    inactives = discord.SlashCommandGroup(name="inactives",
                                          default_member_permissions=discord.Permissions(kick_members=True))

    @tasks.loop(hours=1)
    async def auto_kicker(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(715969701771083817)
        if not guild:
            self.auto_kicker.stop()
            return
        to_be_kicked = (await utils.get_inactives(guild)).get("kickworthy")
        for member in to_be_kicked:
            try:
                await member.send(
                    "You've been kicked from The Paw Kingdom for being inactive for too long. You can rejoin and restart the verification process.")
            except (discord.HTTPException, discord.Forbidden):
                pass
            try:
                await member.kick(reason="Inactive Member")
                await utils.log_member_kick(member, "Inactive")
            except discord.Forbidden:
                log.warning(f"Failed to kick member {member.global_name}!")

    @inactives.command()
    async def get(self, ctx: discord.ApplicationContext):
        """ Get all inactive members """
        members = (await utils.get_inactives(ctx.guild)).get("unverified")
        members = sorted(members, key=lambda member: member.joined_at)
        await ctx.respond(' '.join([member.mention for member in members]))

    @inactives.command()
    async def pending(self, ctx: discord.ApplicationContext):
        """ Get all non-verified accounts (unsure what that means) """
        output = ""
        for member in ctx.guild.members:
            if member.pending:
                output += " " + member.mention
        if not output:
            output = "No members found!"
        await ctx.respond(output)

    @inactives.command()
    async def calcprune(self, ctx: discord.ApplicationContext):
        """ Calculate number of pruned inactive members """
        prunable_roles = [role for role in ctx.guild.roles if
                          role.flags.in_prompt]  # Get all onboarding-assignable roles
        prunable_roles.append(discord.Object(1165755854730035301))  # Unverified role
        prunable_roles.append(discord.Object(778893728701087744))  # Townsfolk role
        amount = await ctx.guild.estimate_pruned_members(days=30, roles=prunable_roles)
        await ctx.respond(f"A prune with the current settings would kick about {amount} members.")


def setup(bot):
    bot.add_cog(Members(bot))
