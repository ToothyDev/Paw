import discord
from discord import option
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
        to_be_kicked = utils.get_inactives(guild).get("kickworthy")
        for member in to_be_kicked:
            try:
                components = [
                    discord.ui.TextDisplay(
                        "You've been kicked from The Paw Kingdom for not reaching level 1 in time to verify yourself "
                        "You can rejoin and restart the verification process using the button below."),
                    discord.ui.ActionRow(
                        discord.ui.Button(label="Rejoin", style=discord.ButtonStyle.link, url="https://discord.gg/tpk"))
                ]
                await member.send(view=discord.ui.DesignerView(*components))
            except (discord.HTTPException, discord.Forbidden):
                pass
            try:
                await member.kick(reason="Inactive Member")
                await utils.log_member_kick(member, "Inactive")
            except discord.Forbidden:
                log.warning(f"Failed to kick member {member.global_name}!")

        # Run spammer kicker on every member after kicking all inactive members
        guild = self.bot.get_guild(715969701771083817)
        for member in guild.members:
            if not any(role.id in utils.INACTIVE_ROLES for role in member.roles):  # If member doesn't have a level role
                await utils.spammer_kicker(member)

    @inactives.command()
    async def get(self, ctx: discord.ApplicationContext):
        """ Get all inactive members """
        inactives = utils.get_inactives(ctx.guild)
        members = sorted(inactives['unverified'], key=lambda member: member.joined_at)
        await ctx.respond(" ".join([member.mention for member in members]) if members else "No unverified members!")

    @inactives.command()
    async def pending(self, ctx: discord.ApplicationContext):
        """ Get all non-verified accounts (unsure what that means) """
        output = " ".join([member.mention for member in ctx.guild.members if member.pending])
        await ctx.respond(output if output else "No pending members!")

    @inactives.command()
    @option("ignored_roles", str, default=None)
    async def calcprune(self, ctx: discord.ApplicationContext, ignored_roles=None):
        """ Calculate number of pruned inactive members """
        # Get all onboarding-assignable roles
        prunable_roles = [role for role in ctx.guild.roles if role.flags.in_prompt]

        if ignored_roles:
            ignored_roles = discord.utils.raw_role_mentions(ignored_roles)
            for role_id in ignored_roles:
                prunable_roles.append(ctx.guild.get_role(role_id))

        prunable_roles.extend([
            ctx.guild.get_role(1165755854730035301),  # Unverified role
            ctx.guild.get_role(778893728701087744)  # Townsfolk role
        ])
        amount = await ctx.guild.estimate_pruned_members(days=30, roles=prunable_roles)
        await ctx.respond(f"A prune with the current settings would kick about {amount} members.")


def setup(bot):
    bot.add_cog(Members(bot))
