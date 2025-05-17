import discord
import openai
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
            await ctx.respond(f"{config.crossmark} **You are missing {perms} permissions.**", ephemeral=True)
            return

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            await ctx.respond(f"{config.crossmark} **I'm missing {perms} permissions**", ephemeral=True)
            return

        if isinstance(err, commands.CommandOnCooldown):
            await ctx.respond(
                f"{config.crossmark} **This command is on cooldown for {round(err.retry_after)} more seconds.**",
                ephemeral=True)
            return

        if isinstance(err, commands.MemberNotFound):
            await ctx.respond(f"{config.confused} **Could not find user `{err.argument}`", ephemeral=True)
            return

        if isinstance(err, discord.NotFound):
            await ctx.respond("I could not find the argument you have provided.", ephemeral=True)
            return

        err = err.original  # Unwrap the exception to catch any non-discord errors

        if isinstance(err, openai.RateLimitError):
            log.info("AI API ratelimit error")
            await ctx.respond("You are using this command too much! Please try again in a few seconds", ephemeral=True)
            return

        if isinstance(err, openai.BadRequestError):
            if err.message == "context deadline exceeded":
                await ctx.respond("The request has timed out! Please try again", ephemeral=True)
                return

        if isinstance(err, openai.InternalServerError):
            log.info("AI API internal service error")
            await ctx.respond("The service this command uses had an error. Try again later.", ephemeral=True)
            return

        if isinstance(err, openai.APIStatusError):
            if err.message.startswith("Request too large for model"):
                log.info("AI API request too large for model")
                await ctx.respond("The chat history is too big! Try again later.", ephemeral=True)
                return

        if isinstance(err, pydantic.ValidationError):
            log.info("AI API pydantic model validation error")
            await ctx.respond("There was an issue generating your sona, try again!", ephemeral=True)
            return

        await ctx.respond("An unknown error occured! This will be logged and fixed!", ephemeral=True)
        log.error(
            f"{ctx.author.global_name} used /{ctx.command} which caused '{err}', error class: {err.__class__.__name__}",
            exc_info=(type(err), err, err.__traceback__))


def setup(bot):
    bot.add_cog(Error(bot))
