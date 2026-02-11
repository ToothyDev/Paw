import io
import logging
import zipfile

import discord
from discord import option, slash_command, RawReactionActionEvent

import utils
from utils.staff_helpers import AssetDownloader

log = logging.getLogger(__name__)


class Staff(discord.Cog, name="Staff"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if payload.guild_id != 715969701771083817:
            return
        member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
        if not member:
            return
        channel = member.guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        embed = discord.Embed(color=utils.Colors.ORANGE)
        embed.set_author(name=f"Reaction was removed | {member.display_name}",
                         icon_url=member.display_avatar.url)
        embed.description = (f"**User**: {member.mention}\n**User ID**: {member.id}\n**Reaction:** {payload.emoji}"
                             f"\n**Message**: {message.jump_url}")
        logchannel = member.guild.get_channel(760181839033139260)
        await logchannel.send(embed=embed)

    @slash_command()
    @discord.default_permissions(manage_guild=True)
    @discord.option("assets", choices=["all", "emojis", "role icons", "stickers"], default="all")
    async def asset_downloader(self, ctx: discord.ApplicationContext, assets: str):
        """ Download this server's emojis, stickers and role icons"""
        interaction = await ctx.respond("Downloading, this might take some time... (0%)")
        zip_buffer = io.BytesIO()  # Create a BytesIO object to hold the ZIP file
        with zipfile.ZipFile(zip_buffer, 'w') as zipped_f:  # Create a ZIP file inside the buffer
            downloader = AssetDownloader(zipped_f, ctx.guild, interaction)
            match assets:
                case "all":
                    await downloader.download_all()
                case "emojis":
                    await downloader.download_emojis()
                case "role icons":
                    await downloader.download_role_icons()
                case "stickers":
                    await downloader.download_stickers()

        await interaction.edit_original_response(content="Uploading assets...")
        zip_buffer.seek(0)  # Reset the buffer position to the beginning so the next line reads the file from the start
        await interaction.edit_original_response(content="Here are all assets of this guild!",
                                                 file=discord.File(zip_buffer, filename="assets.zip"))

    @slash_command()
    @option("day", int, description="Select the desired day of a month", min_value=1, max_value=31)
    @option("month", int, description="Select the desired month number", min_value=1, max_value=12)
    @discord.default_permissions(ban_members=True)
    async def botcollector(self, ctx: discord.ApplicationContext, day: int, month: int):
        """ Get members created on a certain day """
        if day == 0 or month == 0:
            await ctx.respond("0 is not a valid number!")
            return
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
    @option("container", bool, description="Whether to send it as a container", required=False)
    @option("attachment", discord.Attachment, description="An image for the announcement", required=False)
    @discord.default_permissions(manage_guild=True)
    async def announce(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, message: str,
                       container: bool = False, attachment: discord.Attachment = None):
        """ Announce something in a channel """
        if not channel.can_send():
            await ctx.respond(f"I don't have permissions to send messages to {channel.mention}!", ephemeral=True)
            return
        file = None
        if attachment:
            await ctx.defer(ephemeral=True)
            file = await attachment.to_file()
        if container:
            container = discord.ui.Container(discord.ui.TextDisplay(message), color=discord.Color.random())
            if attachment:
                container.add_item(
                    discord.ui.MediaGallery(discord.MediaGalleryItem(url=f"attachment://{attachment.filename}")))
            await channel.send(view=discord.ui.DesignerView(container), file=file)
        else:
            await channel.send(message, file=file)
        await ctx.respond("Message successfully sent!", ephemeral=True)

    @discord.message_command(name="GIF blamer")
    async def gif_blamer(self, ctx: discord.ApplicationContext, message: discord.Message):
        await ctx.respond(message.components[0].components[1].items[0].url)


def setup(bot):
    bot.add_cog(Staff(bot))
