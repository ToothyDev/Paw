from discord.ext import commands, bridge
import random
import discord
import data


class utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(brief="Generate a sona!")
    async def sonagen(self, ctx):
        primary_color = random.randint(0x000000, 0xFFFFFF)
        color = random.choice(data.colors)
        species = random.choice(data.species)
        sonatype = random.choice(["Feral", "Anthro"])
        sex = random.choice(["Male", "Male", "Male", "Male", "Female", "Female", "Female", "Female", "Hermaphrodite"])

        embed=discord.Embed(title="Your Sona:", color = primary_color)
        embed.add_field(name="Species:", value=f"{sonatype} {species}", inline=True)
        embed.add_field(name="Primary Color:", value=f"#{'{:06x}'.format(primary_color)} (embed color)", inline=True)
        embed.add_field(name="Secondary Color:", value=color, inline=True)
        if sonatype == "Feral":
            embed.add_field(name="Height to shoulders:", value=f"{random.randint(20,140)}cm", inline=True)
        else:
            embed.add_field(name="Height:", value=f"{random.randint(120,240)}cm", inline=True)
        
        embed.add_field(name="Sex:", value=sex, inline=True)
        

        return await ctx.respond("Sure, here's your freshly generated sona!", embed=embed)
    

def setup(bot):
    bot.add_cog(utility(bot))
