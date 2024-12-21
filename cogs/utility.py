import json
import random
import config # Help?

import discord
import psutil
from discord import option, slash_command

import assets
import logger
import utils

log = logger.get_logger(__name__)


class Utility(discord.Cog, name="Utilities"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.ai_enabled = utils.is_ai_enabled()

    @slash_command(contexts={discord.InteractionContextType.guild})
    @option("species", str, description="The species of the fursona", required=False)
    @option("sex", str, description="The sex of the fursona", choices=["Male", "Female", "Intersex"], required=False)
    @option("type", str, description="The type of the fursona", parameter_name="sonatype", choices=["Feral", "Anthro"],
            required=False)
    async def sonagen(self, ctx: discord.ApplicationContext, species: str, sex: str, sonatype: str):
        """ Generate a random sona """
        if not self.ai_enabled:
            return await ctx.respond("AI functions are disabled due to missing (or invalid) API key, please contact the bot owner to fix this.")
        await ctx.defer()
        primary_color = discord.Color.random()
        color = random.choice(utils.data.COLOR_STRINGS)

        sona = await utils.api_helpers.generate_sona(
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

        name = sona.name
        sonatype = sona.type
        species = sona.species
        sex = sona.gender
        height = sona.height
        description = sona.description
        heightstring = f"**Height{' to shoulders' if sonatype == 'Feral' else ''}**: {height}cm"

        embed = discord.Embed(title="Your Sona:", color=primary_color, description=f"""
**Name**: {name}
**Species**: {sonatype} {species}
**Primary Color**: {str(primary_color)} (embed color)
**Secondary Color**: {color}
{heightstring}
**Sex**: {sex}
**Description**: {description}
        """)
        await ctx.respond(content="Sure, here's your freshly generated sona!", embed=embed)

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
        ram = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        divamount = 1_000_000_000

        user_count = len(self.bot.users)
        latency = round(self.bot.latency * 1000)
        used_ram = round((ram.used / divamount), 2)
        total_ram = round((ram.total / divamount), 2)
        percent_used_ram = round(((ram.used / ram.total) * 100), 2)
        free_disk = round((disk_usage.free / divamount), 2)
        total_disk = round((disk_usage.total / divamount), 2)
        percent_free_disk = round((((disk_usage.used / disk_usage.total * 100) - 100) * (-1)), 2)

        embed = discord.Embed(color=utils.Colors.BLUE)
        embed.description = f"""
{self.bot.user.name} is a bot developed by TPK to provide social interaction commands and other fun things!
**Users:** {user_count}
**API Latency:** {latency}ms
**RAM:** {used_ram}GB used out of {total_ram}GB total ({percent_used_ram}% used)
**Disk:** {free_disk}GB free out of {total_disk}GB total ({percent_free_disk}% free)

[[Github]](https://github.com/ToothyDev/Paw)"""
        await ctx.respond(embed=embed)

    @slash_command()
    async def paw(self, ctx: discord.ApplicationContext):
        """ Get random art of me, Paw """
        embed = discord.Embed(title="A picture of myself, Paw!", color=utils.Colors.BLUE)
        embed.set_image(url=random.choice(assets.PAW))
        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Utility(bot))
