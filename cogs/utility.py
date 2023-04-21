from discord.ext import commands, bridge
import random
import discord
import data


class utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @bridge.bridge_command(brief="Generate a sona!")
    async def sonagen(self, ctx):
        """ Generate a random sona """
        primary_color = random.randint(0x000000, 0xFFFFFF)
        color = random.choice(data.colors)
        species = random.choice(list(data.species))
        sonatype = random.choice(["Feral", "Anthro"])
        sex = random.choice(["Male", "Male", "Male", "Male", "Female", "Female", "Female", "Female", "Hermaphrodite"])

        if sonatype == "Feral":
            heightstring = f"**Height to shoulders**: {random.randint(data.species[species][0], data.species[species][1])}cm"
        else:
            heightstring = f"**Height**: {random.randint(130, 240)}cm"

        embed = discord.Embed(title="Your Sona:", color=primary_color, description=f"""
**Species**: {sonatype} {species}
**Primary Color**: #{'{:06x}'.format(primary_color)} (embed color)
**Secondary Color**: {color}
{heightstring}
**Sex**: {sex}
""")

        return await ctx.respond("Sure, here's your freshly generated sona!", embed=embed)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.is_owner()
    @bridge.bridge_command(brief="Get rid of bots")
    async def botcollector(self, ctx, day: int, month: int):
        output = ""
        guild = self.bot.get_guild(ctx.guild.id)
        async for member in guild.fetch_members():
            if not member.bot:
                if member.created_at.day == day and member.created_at.month == month:
                    output += f"{member.mention} "
        message = await ctx.respond("Fetching...")
        await message.edit_original_response(content=output)


def setup(bot):
    bot.add_cog(utility(bot))
