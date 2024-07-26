import io
import json
import random
import zipfile

import aiohttp
import discord
import groq
import psutil
from discord import option, slash_command

import assets
import utils
from views import ConfirmView


class Utility(discord.Cog, name="Utilities"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command()
    @option("species", str, description="The species of the fursona", required=False)
    @option("sex", str, description="The sex of the fursona", choices=["Male", "Female", "Intersex"], required=False)
    @option("type", str, description="The type of the fursona", parameter_name="sonatype", choices=["Feral", "Anthro"],
            required=False)
    async def sonagen(self, ctx: discord.ApplicationContext, species: str, sex: str, sonatype: str):
        """ Generate a random sona """
        await ctx.defer()
        primary_color = discord.Color.random()
        color = random.choice(utils.data.colors)
        
        try:
            response = await utils.api_helpers.generate_sona(
                f"""Your job is to generate a fursona as a fursona generator. Use the following json schema: {json.dumps(utils.data.Fursona.model_json_schema(), indent=2)}
                The user already picked the following values:
                {species if species else ""} {sex if sex else ""} {sonatype if sonatype else ""}
                Do NOT change the values the user picked, instead, use them as is and generate the sona using them
                You should however "clean" the species name, e.g. correct typos and remove unnecessary bits. Start with a capital letter.
                Also, do NOT let the species name influence your following choices. Pick that on your own.
                Make up a name that may incorporate any of the sona's attributes, but does not have to.
                The species is any animal that makes sense as a fursona.
                The sona type is either Feral or Anthro.
                Gender may be Male, Feral or Intersex, but pick Intersex only rarely.
                Color: {primary_color}.
                Secondary Color: {color}.
                Standing Height in cm (shoulder height for feral sonas).
                Consider a height of 175cm average / normal for anthro sonas.
                For feral sonas, pick a shoulder height that is reasonable for the animal you chose.
                Generate a small, 2-3 sentence fursona description based on the following values:
                Always add a description of their physical features, traits or behaviours, never simply describe their "stats".
                Always say colors by name and not in hexadecimal form.
                Do not say anything towards the user, simply act like a sona text generator""")
        except groq.RateLimitError as e:
            return await ctx.respond(f"You are using this command too much! {e.message.split('.')[1]}s")
        except Exception as e:
            return await ctx.respond(f"Something went wrong! Error: {e}")

        name = response.name
        sonatype = response.type
        species = response.species
        sex = response.gender
        height = response.height

        heightstring = f"**Height{' to shoulders' if sonatype == 'Feral' else ''}**: {height}cm"

        embed = discord.Embed(title="Your Sona:", color=primary_color, description=f"""
**Name**: {name}
**Species**: {sonatype} {species}
**Primary Color**: {str(primary_color)} (embed color)
**Secondary Color**: {color}
{heightstring}
**Sex**: {sex}
**Description**: {response.description}
        """)
        await ctx.respond(content=f"Sure, here's your freshly generated sona!", embed=embed)

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
    async def serverinfo(self, ctx: discord.ApplicationContext):
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
        embed.colour = utils.Colors.blue
        await ctx.respond(embed=embed)

    @slash_command()
    async def paw(self, ctx: discord.ApplicationContext):
        """ Get random art of me, Paw """
        embed = discord.Embed(title="A picture of myself, Paw!", color=utils.Colors.blue)
        embed.set_image(url=random.choice(assets.paw))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
