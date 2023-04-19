from discord.ext import commands, bridge
import random
import discord
import data


class utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(brief="Generate a sona!")
    async def sonagen(self, ctx):
        """ Generate a random sona """
        primary_color = random.randint(0x000000, 0xFFFFFF)
        color = random.choice(data.colors)
        species = random.choice(data.species)
        sonatype = random.choice(["Feral", "Anthro"])
        sex = random.choice(["Male", "Male", "Male", "Male", "Female", "Female", "Female", "Female", "Hermaphrodite"])
        if sonatype == "Feral":
            heightstring = f"**Height to shoulders**: {random.randint(20,140)}cm"
        else:
            heightstring = f"**Height**: {random.randint(120,240)}cm"

        embed=discord.Embed(title="Your Sona:", color=primary_color, description=f"""
            **Species**: {sonatype} {species}
            **Primary Color**: #{'{:06x}'.format(primary_color)} (embed color)
            **Secondary Color**: {color}
            {heightstring}
            **Sex**: {sex}
            """)

        return await ctx.respond("Sure, here's your freshly generated sona!", embed=embed)
    

def setup(bot):
    bot.add_cog(utility(bot))
