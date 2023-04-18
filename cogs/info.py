from discord.ext import commands, bridge
from discord import Embed
from utils import Colors
import psutil


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["information", "ping", "latency", "pong", "servers", "guilds", "support", "invite"], description=f"Displays information about Paw")
    async def info(self, ctx):
        embed = Embed()
        embed.description = f"""
{self.bot.user.name} is a bot developed by TPK to provide social interaction commands and other fun things!

**Guilds:** {len(self.bot.guilds)}
**Users:** {sum(x.member_count for x in self.bot.guilds)}
**API Latency:** {round(self.bot.latency * 1000)}ms
**RAM:** {psutil.virtual_memory().used / 1000000000} used out of {psutil.virtual_memory().total / 1000000000}GB total ({psutil.virtual_memory().percent}% used)
**Disk:** {psutil.disk_usage('/').free / 1000000000} free out of {psutil.disk_usage('/').total / 1000000000}GB total ({((psutil.disk_usage('/').percent) - 100)*(-1)}% free)

[[Github]](https://github.com/MiataBoy/iLoveMiatas) [[Privacy Policy]](https://gist.github.com/MiataBoy/20fda9024f277ea5eb2421adbebc2f23) [[Terms of Service]](https://gist.github.com/MiataBoy/81e96023a2aa055a038edab02e7e7792)
        """
        embed.colour = Colors.blue
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
