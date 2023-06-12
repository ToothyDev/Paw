from discord.ext import commands, bridge
from discord import Embed
from utils import Colors
import psutil

class Info(commands.Cog):
    def __init__(self, bot: bridge.Bot):
        self.bot = bot

    @bridge.bridge_command(aliases=["information", "ping", "latency", "pong", "servers", "guilds", "support", "invite"], description=f"Displays information about Paw")
    async def info(self, ctx: bridge.BridgeContext):
        embed = Embed()
        vram = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        divamount = 1000000000
        embed.description = f"""
{self.bot.user.name} is a bot developed by TPK to provide social interaction commands and other fun things! Sponsored by [Blue Atomic](https://github.com/BlueAtomic)
**Users:** {len(self.bot.get_all_members())}
**API Latency:** {round(self.bot.latency * 1000)}ms
**RAM:** {round((vram.used / divamount), 2)}GB used out of {round((vram.total / divamount), 2)}GB total ({vram.percent}% used)
**Disk:** {round((disk_usage.free / divamount), 2)}GB free out of {round((disk_usage.total / divamount), 2)}GB total ({(disk_usage.percent - 100) * (-1)}% free)

[[Github]](https://github.com/MiataBoy/Paw) [[Privacy Policy]](https://gist.github.com/MiataBoy/20fda9024f277ea5eb2421adbebc2f23) [[Terms of Service]](https://gist.github.com/MiataBoy/81e96023a2aa055a038edab02e7e7792)
        """
        embed.colour = Colors.blue
        await ctx.respond(embed=embed)


def setup(bot: bridge.Bot):
    bot.add_cog(Info(bot))
