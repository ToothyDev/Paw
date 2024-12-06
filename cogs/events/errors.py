import discord
import groq
import pydantic
from discord.ext import commands

import config
import logger

log = logger.get_logger(__name__)


class Error(discord.Cog, name="Errors"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext,
                                           err: discord.ApplicationCommandInvokeError):
        if isinstance(err, commands.MissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.respond(f"{config.crossmark} **You are missing {perms} permissions.**", ephemeral=True)

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.respond(f"{config.crossmark} **I'm missing {perms} permissions**", ephemeral=True)

        if isinstance(err, commands.CommandOnCooldown):
            return await ctx.respond(
                f"{config.crossmark} **This command is on cooldown for {round(err.retry_after)} more seconds.**",
                ephemeral=True)

        if isinstance(err, commands.MemberNotFound):
            return await ctx.respond(f"{config.confused} **Could not find user `{err.argument}`", ephemeral=True)

        if isinstance(err, discord.NotFound):
            return await ctx.respond("I could not find the argument you have provided.", ephemeral=True)

        err = err.original  # Unwrap the exception to catch any non-discord errors

        if isinstance(err, groq.RateLimitError):
            log.info("Groq API ratelimit error")
            return await ctx.respond(f"You are using this command too much! {err.message.split('.')[1]}s",
                                     ephemeral=True)

        if isinstance(err, groq.BadRequestError):
            if err.message == "context deadline exceeded":
                return await ctx.respond("The request has timed out! Please try again", ephemeral=True)

        if isinstance(err, groq.InternalServerError):
            log.info("Groq API internal service error")
            return await ctx.respond("The service this command uses had an error. Try again later.", ephemeral=True)

        if isinstance(err, groq.APIStatusError):
            if err.message.startswith("Request too large for model"):
                log.info("Groq API request too large for model")
                return await ctx.respond("The chat history is too big! Try again later.", ephemeral=True)

        if isinstance(err, pydantic.ValidationError):
            log.info("Groq API pydantic model validation error")
            return await ctx.respond("There was an issue generating your sona, try again!", ephemeral=True)

        await ctx.respond("An unknown error occured! This will be logged and fixed!", ephemeral=True)
        log.error(
            f"{ctx.author.global_name} used /{ctx.command} which caused '{err}' - Error class: {err.__class__.__name__}",
            exc_info=(type(err), err, err.__traceback__))


def setup(bot):
    bot.add_cog(Error(bot))
