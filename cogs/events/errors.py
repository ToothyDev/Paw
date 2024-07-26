import discord
import groq
from discord.ext import commands

import config


class Error(commands.Cog, name="Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext,
                                           err: discord.DiscordException | groq.APIError):
        if isinstance(err, commands.MissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.respond(f"{config.crossmark} **You are missing {perms} permissions.**", ephemeral=True)

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.respond(f"{config.crossmark} **I'm missing {perms} permissions**", ephemeral=True)

        if isinstance(err, commands.CommandOnCooldown):
            return await ctx.respond(f"{config.crossmark} **This command is on cooldown for {round(err.retry_after)} more seconds.**", ephemeral=True)

        if isinstance(err, commands.MemberNotFound):
            return await ctx.respond(f"{config.confused} **Could not find user `{err.argument}`", ephemeral=True)

        if isinstance(err, discord.NotFound):
            return await ctx.respond("I could not find the argument you have provided.", ephemeral=True)

        if isinstance(err, groq.RateLimitError):
            return await ctx.respond(f"You are using this command too much! {err.message.split('.')[1]}s")

        await ctx.respond("An unknown error occured! This will be logged and fixed!", ephemeral=True)
        print(err)


def setup(bot):
    bot.add_cog(Error(bot))
