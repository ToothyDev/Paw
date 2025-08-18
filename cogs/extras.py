import discord
from discord import option

import utils
from views.basic_image_view import BasicImageView


class Extras(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        base_url = "https://api.some-random-api.com"

        self.filter_group = discord.SlashCommandGroup("filter", "Filter commands")
        self.border_group = discord.SlashCommandGroup("border", "Border commands")
        self.overlay_group = discord.SlashCommandGroup("overlay", "Overlay commands")

        for command in utils.data.FILTER_COMMANDS_DATA:
            self._create_image_command(command["name"], base_url + command["url"], self.filter_group)
        for command in utils.data.BORDER_COMMANDS_DATA:
            self._create_image_command(command["name"], base_url + command["url"], self.border_group)
        for command in utils.data.OVERLAY_COMMANDS_DATA:
            self._create_image_command(command["name"], base_url + command["url"], self.overlay_group)

        self.bot.add_application_command(self.filter_group)
        self.bot.add_application_command(self.border_group)
        self.bot.add_application_command(self.overlay_group)

    def _create_image_command(self, name: str, endpoint_url: str, group):
        @group.command(name=name, description=f"Apply a {name} filter to a user's avatar!")
        @option("member", discord.Member, description=f"The user to apply the {group.name} to!", required=False)
        async def command_function(_cog: Extras, ctx: discord.ApplicationContext, member: discord.Member):
            if not member:
                member = ctx.author
            final_url = endpoint_url + "?avatar=" + member.display_avatar.with_format("png").url
            await ctx.respond(view=BasicImageView(final_url))

        command_function.cog = self


def setup(bot):
    bot.add_cog(Extras(bot))
