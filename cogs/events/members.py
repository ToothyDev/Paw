from discord.ext import commands
import utils
import time


class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot
        self.memberkicker = utils.AutoVerify(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 715969701771083817:
            self.memberkicker.addMember((member.id, time.time()))


def setup(bot):
    bot.add_cog(Members(bot))
