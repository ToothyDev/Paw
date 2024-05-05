import io
import random
import zipfile

import aiohttp
import discord
import psutil
from discord import option, slash_command
from discord.ext import commands

import ai_handler
import data
from utils import Colors
from views import ConfirmView


class Utility(discord.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @option("species", str, choices=data.species, required=False, default=random.choice(list(data.species)))
    @option("sex", str, choices=["Male", "Female", "Intersex"], required=False,
            default=random.choice(["Male", "Male", "Male", "Male", "Female", "Female", "Female", "Female", "Intersex"]))
    @option("type", str, parameter_name="sonatype", choices=["Feral", "Anthro"], required=False,
            default=random.choice(["Feral", "Anthro"]))
    async def sonagen(self, ctx, species, sex, sonatype):
        """ Generate a random sona """
        await ctx.defer()
        primary_color = discord.Color.random()
        color = random.choice(data.colors)
        if sonatype == "Feral":
            heightstring = f"**Height to shoulders**: {random.randint(data.species[species][0], data.species[species][1])}cm"
        else:
            heightstring = f"**Height**: {random.randint(130, 240)}cm"
        response = await ai_handler.generate_single(
            f"""Generate a small, 2-3 sentence fursona description based on the following values:
            Species: {species}.
            Sona type: {sonatype}.
            Gender: {sex}.
            Color: {primary_color}.
            Secondary Color: {color}.
            Standing Height in cm (shoulder height for feral sonas): {heightstring}.
            Consider a height of 175cm average / normal for anthro sonas.
            The user already knows all of these values, so just make an accompanying description to make it come alive!
            Always add a description of their physical features, traits or behaviours, never simply describe their "stats".
            Finally, make up a name that may incorporate any of the sona's attributes, but does not have to.
            Always say colors by name and not in hexadecimal form.
            Return your output seperated by ; in the following order: Name;Description
            Do not add any extras to the name, simply state the name
            Do not say anything towards the user, simply act like a sona text generator""")
        name = response.split(";")[0]
        embed = discord.Embed(title="Your Sona:", color=primary_color, description=f"""
        **Name**: {name}
        **Species**: {sonatype} {species}
        **Primary Color**: {str(primary_color)} (embed color)
        **Secondary Color**: {color}
        {heightstring}
        **Sex**: {sex}
        **Description**: {response.split(";")[1]}
        """)
        await ctx.respond(content=f"Sure, here's your freshly generated sona!", embed=embed)

    @slash_command()
    @discord.default_permissions(manage_guild=True)
    async def emoji_downloader(self, ctx):
        """ Download this server's emojis and stickers """
        saved_emojis = []
        saved_stickers = []
        total = len(ctx.guild.emojis) + len(ctx.guild.stickers)
        current = 0
        message = await ctx.respond(f"Downloading, this might take some time... (0 of {total})")
        zip_buffer = io.BytesIO()  # Create a BytesIO object to hold the ZIP file
        with zipfile.ZipFile(zip_buffer, 'w') as zipped_f:  # Create a ZIP file inside the buffer
            for emoji in ctx.guild.emojis:
                emoji_file_name = (emoji.name if emoji.name not in saved_emojis else emoji.name + str(saved_emojis.count(emoji.name) + 1)) + emoji.url[-4:]
                zipped_f.writestr(f"emojis/{emoji_file_name}", await emoji.read())
                saved_emojis.append(emoji.name)
                current += 1
                await message.edit_original_response(content=f"Downloading, this might take some time... ({current} of {total})")

            async with aiohttp.ClientSession() as session:
                for sticker in ctx.guild.stickers:
                    async with session.get(sticker.url) as response:
                        sticker_file_name = (sticker.name if sticker.name not in saved_stickers else sticker.name + str(saved_stickers.count(sticker.name) + 1)) + ".png"
                        zipped_f.writestr(f"stickers/{sticker_file_name}", await response.read())
                        saved_stickers.append(sticker.name)

        zip_buffer.seek(0)  # Reset the buffer position to the beginning so the next line reads the file from the start
        await message.edit_original_response(content="Here are all emojis and stickers of this guild!", file=discord.File(zip_buffer, filename="emojis_and_stickers.zip"))

    @slash_command()
    @option("day", int, description="Select the desired day of a month", min_value=1, max_value=31)
    @option("month", int, description="Select the desired month number", min_value=1, max_value=12)
    @discord.default_permissions(ban_members=True)
    async def botcollector(self, ctx, day: int, month: int):
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
    @option("channel", discord.TextChannel, description="The channel to announce in")
    @option("message", str, description="The message to announce")
    @option("embed", bool, description="Whether to make it an embed", required=False, default=False)
    @option("attachment", discord.Attachment, description="A nice image", required=False, default=None)
    @discord.default_permissions(manage_guild=True)
    async def announce(self, ctx, channel: discord.TextChannel, message: str, embed: bool, attachment: discord.Attachment):
        """ Announce something in a channel """
        await ctx.defer(ephemeral=True)
        if not channel.can_send():
            return await ctx.respond(f"I don't have permissions to send messages to {channel.mention}!", ephemeral=True)
        if embed:
            view = ConfirmView()
            await ctx.respond("Are you sure? Embeds don't actually send pings to any roles or users", view=view, ephemeral=True)
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

    @slash_command()
    async def serverinfo(self, ctx):
        """ Get the current server's info """
        guild = ctx.guild
        owner = await discord.utils.get_or_fetch(guild, 'member', guild.owner_id)
        embed = discord.Embed(color=discord.Color.random(), title=guild.name)
        embed.description = f"""
**Owner:** {owner.mention}
**Members:** {guild.member_count}
**Roles:** {len(guild.roles)}
**Verification:** {str(guild.verification_level).title()}
**Channels:** {len(guild.text_channels)} Text, {len(guild.voice_channels)} Voice
**Created:** <t:{round(guild.created_at.timestamp())}:R>
**Emojis:** {len(guild.emojis)}
**Stickers:** {len(guild.stickers)}
        """
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"ID: {guild.id}")
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        features = ", ".join(guild.features).replace("_", " ").title()
        embed.add_field(name="Features", value=features)
        await ctx.respond(embed=embed)

    @slash_command()
    async def info(self, ctx: discord.ApplicationContext):
        """ Displays information about Paw """
        embed = discord.Embed()
        vram = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        divamount = 1000000000
        embed.description = f"""
{self.bot.user.name} is a bot developed by TPK to provide social interaction commands and other fun things! Sponsored by [Blue Atomic](https://github.com/BlueAtomic)
**Users:** {sum(x.member_count for x in self.bot.guilds)}
**API Latency:** {round(self.bot.latency * 1000)}ms
**RAM:** {round((vram.used / divamount), 2)}GB used out of {round((vram.total / divamount), 2)}GB total ({round(((vram.used / vram.total) * 100), 2)}% used)
**Disk:** {round((disk_usage.free / divamount), 2)}GB free out of {round((disk_usage.total / divamount), 2)}GB total ({round((((disk_usage.used / disk_usage.total * 100) - 100) * (-1)), 2)}% free)

[[Github]](https://github.com/MiataBoy/Paw) [[Privacy Policy]](https://gist.github.com/MiataBoy/20fda9024f277ea5eb2421adbebc2f23) [[Terms of Service]](https://gist.github.com/MiataBoy/81e96023a2aa055a038edab02e7e7792)
        """
        embed.colour = Colors.blue
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
