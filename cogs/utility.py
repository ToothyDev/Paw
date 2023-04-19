from discord.ext import commands, bridge
import random
import discord


class utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(brief="Generate a sona!")
    async def sonagen(self, ctx):
        primary_color = hex(random.randrange(0, 2**24))
        colors = ["Red", "Green", "Blue", "Pink", "Purple", "Brown", "Black", "White", "Orange", "Teal", "Light Green", "Light Blue", "Grey", "Yellow"]
        species = ["Dragon", "Fox", "Deer", "Wolf", "Dog", "Bunny", "Protogen", "Hyena", "Tiger", "Lion", "Bird", "Otter", "Snake", "Cat", "Sergal", "Horse", "Shark", "Lizard"]
        sonatype = random.choice(["Feral", "Anthro"])
        sex = ["Male", "Male", "Male", "Male", "Female", "Female", "Female", "Female", "Hermaphrodite"]

        embed=discord.Embed(title="Your Sona:", color=primary_color)
        embed.add_field(name="Primary Color:", value=f"{primary_color} (see embed color)", inline=True)
        embed.add_field(name="Secondary Color:", value=random.choice(colors), inline=True)
        embed.add_field(name="Species:", value=f"{random.choice(sonatype)} {random.choice(species)}", inline=True)
        embed.add_field(name="Sex:", value=random.choice(sex), inline=True)
        if sonatype == "Feral":
            embed.add_field(name="Length:", value=f"{random(80,560)}cm", inline=True)
        else:
            embed.add_field(name="Height:", value=f"{random(120,240)}cm", inline=True)

        return await ctx.respond("Sure, here's your freshly generated sona!", embed=embed)


def setup(bot):
    bot.add_cog(utility(bot))
