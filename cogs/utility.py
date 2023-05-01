from discord.ext import commands, bridge
import random
import discord
from discord import option
import data


class utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(brief="Generate a sona!")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def sonagen(self, ctx):
        """ Generate a random sona """
        primary_color = discord.Color.random()
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
**Primary Color**: {str(primary_color)} (embed color)
**Secondary Color**: {color}
{heightstring}
**Sex**: {sex}
""")

        return await ctx.respond("Sure, here's your freshly generated sona!", embed=embed)

    @bridge.bridge_command(brief="Get rid of bots")
    @option("day", int, description="Select the desired day of a month", min_value=1, max_value=31)
    @option("month", int, description="Select the desired month number", min_value=1, max_value=12)
    @bridge.has_permissions(ban_members=True)
    async def botcollector(self, ctx, day: int, month: int):
        """ Get members created on a certain day """
        if day == 0 or month == 0:
            return await ctx.respond("0 is not a valid number!")
        output = ""
        guild = self.bot.get_guild(ctx.guild.id)
        message = await ctx.respond("Fetching...")
        async for member in guild.fetch_members():
            if not member.bot:
                if member.created_at.day == day and member.created_at.month == month:
                    output += f"{member.mention} "
        if output == "":
            output = "No one found!"
        await message.edit_original_response(content=output)

    @bridge.bridge_command(brief="Announce something!")
    @option("channel", discord.TextChannel, description="The channel to announce in")
    @option("message", str, description="The message to announce")
    @option("embed", bool, description="Whether to make it an embed")
    @bridge.has_permissions(manage_guild=True)
    async def announce(self, ctx, channel: discord.TextChannel, message: str, embed):
        if embed:
            view = ConfirmView()
            await ctx.respond("Are you sure? Embeds don't actually send pings to any roles or users", view=view, ephemeral=True)
            await view.wait()
            if not view.confirmed:
                return
        try:
            if not embed:
                await channel.send(message)
            else:
                embed = discord.Embed(colour=discord.Color.random(), description=message)
                await channel.send(embed=embed)
            if ctx.channel is not channel:
                await ctx.respond("Message successfully sent!", ephemeral=True)
        except Exception as e:
            if str(e).startswith("403"):
                e = "Missing Permissions"
            await ctx.respond(f"Could not send message, `{e}`!\nMake sure I have view and write access in {channel.mention}", ephemeral=True)


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        confirmed: bool = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button, interaction):
        self.confirmed = True
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button, interaction):
        self.confirmed = False
        self.disable_all_items()
        await interaction.response.edit_message(content="Cancelled", view=None)
        self.stop()


def setup(bot):
    bot.add_cog(utility(bot))
