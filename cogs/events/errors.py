import discord
import config
from discord.ext import commands


# from cogs.admin import admin_only

class error(commands.Cog, name="Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            return

        if isinstance(err, commands.MissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.send("{} **You are missing {} permissions.**".format(config.crossmark, perms))

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.send("{} **I'm missing {} permissions**".format(config.crossmark, perms))

        if isinstance(err, commands.MissingRequiredArgument):
            return await ctx.send("{} **`{}` is a required argument!**".format(config.crossmark, err.param.name))

        if isinstance(err, commands.CommandOnCooldown):
            return await ctx.send(
                "{} **This command is on cooldown for __{:.0f}__ more seconds.**".format(config.crossmark,
                                                                                         err.retry_after))

        if isinstance(err, commands.MemberNotFound):
            return await ctx.send("{0} **Could not find user `{1}`**".format(config.confused, err.argument))

        if isinstance(err, discord.NotFound):
            return await ctx.send("I could not find the argument you have provided.")


def setup(bot):
    bot.add_cog(error(bot))
