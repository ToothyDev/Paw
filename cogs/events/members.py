from discord.ext import commands
import utils
import time


class Members(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot
        self.memberkicker = utils.AutoVerify(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"Member joined! {member.name}")
        self.memberkicker.addMember((member.id, member.guild.id, time.time()))


def setup(bot):
    bot.add_cog(Members(bot))
