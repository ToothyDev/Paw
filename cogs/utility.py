import json
import random

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

    @slash_command(contexts={discord.InteractionContextType.guild})
    @option("species", str, description="The species of the fursona", required=False)
    @option("sex", str, description="The sex of the fursona", choices=["Male", "Female", "Intersex"], required=False)
    @option("type", str, description="The type of the fursona", parameter_name="sonatype", choices=["Feral", "Anthro"],
            required=False)
    async def sonagen(self, ctx: discord.ApplicationContext, species: str, sex: str, sonatype: str):
        """ Generate a random sona """
        await ctx.defer()
        primary_color = discord.Color.random()
        color = random.choice(utils.data.COLOR_STRINGS)

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
        embed = discord.Embed()
        vram = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        divamount = 1000000000
        embed.description = f"""
{self.bot.user.name} is a bot developed by TPK to provide social interaction commands and other fun things!
**Users:** {sum(x.member_count for x in self.bot.guilds)}
**API Latency:** {round(self.bot.latency * 1000)}ms
**RAM:** {round((vram.used / divamount), 2)}GB used out of {round((vram.total / divamount), 2)}GB total ({round(((vram.used / vram.total) * 100), 2)}% used)
**Disk:** {round((disk_usage.free / divamount), 2)}GB free out of {round((disk_usage.total / divamount), 2)}GB total ({round((((disk_usage.used / disk_usage.total * 100) - 100) * (-1)), 2)}% free)

[[Github]](https://github.com/ToothyDev/Paw)"""
        embed.colour = utils.Colors.BLUE
        await ctx.respond(embed=embed)

    @slash_command()
    async def paw(self, ctx: discord.ApplicationContext):
        """ Get random art of me, Paw """
        embed = discord.Embed(title="A picture of myself, Paw!", color=utils.Colors.BLUE)
        embed.set_image(url=random.choice(assets.PAW))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
