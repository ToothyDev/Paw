import io
import zipfile

import aiohttp
import discord
from discord import option, slash_command

import logger
from views import ConfirmView

log = logger.get_logger(__name__)


class Staff(discord.Cog, name="Staff"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command()
    @discord.default_permissions(manage_guild=True)
    async def emoji_downloader(self, ctx: discord.ApplicationContext):
        """ Download this server's emojis and stickers """
        saved_emojis = []
        saved_stickers = []
        total = len(ctx.guild.emojis) + len(ctx.guild.stickers)
        current = 0
        message = await ctx.respond(f"Downloading, this might take some time... (0 of {total})")
        zip_buffer = io.BytesIO()  # Create a BytesIO object to hold the ZIP file
        with zipfile.ZipFile(zip_buffer, 'w') as zipped_f:  # Create a ZIP file inside the buffer
            for emoji in ctx.guild.emojis:
                emoji_file_name = (emoji.name if emoji.name not in saved_emojis else emoji.name + str(
                    saved_emojis.count(emoji.name) + 1)) + emoji.url[-4:]
                zipped_f.writestr(f"emojis/{emoji_file_name}", await emoji.read())
                saved_emojis.append(emoji.name)
                current += 1
                await message.edit_original_response(
                    content=f"Downloading, this might take some time... ({current} of {total})")

            async with aiohttp.ClientSession() as session:
                for sticker in ctx.guild.stickers:
                    async with session.get(sticker.url) as response:
                        sticker_file_name = (sticker.name if sticker.name not in saved_stickers else sticker.name + str(
                            saved_stickers.count(sticker.name) + 1)) + ".png"
                        zipped_f.writestr(f"stickers/{sticker_file_name}", await response.read())
                        saved_stickers.append(sticker.name)

        zip_buffer.seek(0)  # Reset the buffer position to the beginning so the next line reads the file from the start
        await message.edit_original_response(content="Here are all emojis and stickers of this guild!",
                                             file=discord.File(zip_buffer, filename="emojis_and_stickers.zip"))

    @slash_command()
    @option("day", int, description="Select the desired day of a month", min_value=1, max_value=31)
    @option("month", int, description="Select the desired month number", min_value=1, max_value=12)
    @discord.default_permissions(ban_members=True)
    async def botcollector(self, ctx: discord.ApplicationContext, day: int, month: int):
        """ Get members created on a certain day """
        if day == 0 or month == 0:
            return await ctx.respond("0 is not a valid number!")
        output = ""
        message = await ctx.respond("Fetching...")
        for member in ctx.guild.members:
            if not member.bot:
                if member.created_at.day == day and member.created_at.month == month:
                    output += f"{member.mention} "
        if output == "":
            output = "No one found!"
        await message.edit_original_response(content=output)

    @slash_command()
    @option("channel", channel_types=[discord.ChannelType.news, discord.ChannelType.text],
            description="The channel to announce in")
    @option("message", str, description="The message to announce")
    @option("embed", bool, description="Whether to make it an embed", required=False, default=False)
    @option("attachment", discord.Attachment, description="A nice image", required=False, default=None)
    @discord.default_permissions(manage_guild=True)
    async def announce(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, message: str, embed: bool,
                       attachment: discord.Attachment):
        """ Announce something in a channel """
        await ctx.defer(ephemeral=True)
        if not channel.can_send():
            return await ctx.respond(f"I don't have permissions to send messages to {channel.mention}!", ephemeral=True)
        if embed:
            view = ConfirmView()
            await ctx.respond("Are you sure? Embeds don't actually send pings to any roles or users", view=view,
                              ephemeral=True)
            await view.wait()
            if not view.confirmed:
                return
            message_embed = discord.Embed(colour=discord.Color.random(), description=message)
            if attachment:
                message_embed.set_image(url=attachment.url)
            await channel.send(embed=message_embed)
        else:
            if attachment:
                file = await attachment.to_file()
                await channel.send(content=message, file=file)
            else:
                await channel.send(message)
        await ctx.respond("Message successfully sent!", ephemeral=True)


def setup(bot):
    bot.add_cog(Staff(bot))
