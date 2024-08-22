import discord

import utils
from utils import Colors


class MemberEvents(discord.Cog, name="Member Events"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await utils.spammer_kicker(member)

    @discord.Cog.listener()
    async def on_member_update(self, member_old: discord.Member, member: discord.Member):
        if not member.guild.id == 715969701771083817:
            return

        if member.bot:  # If member is an ACTUAL bot
            return


        if await utils.userbot_kicker(member):  # If member is a bot (95% accurate)
            return

        await utils.unverified_role_handler(member_old, member)

        if len(member_old.roles) <= 3 < len(member.roles):
            if member.pending:
                return
            if not utils.spammer_kicker(member):
                await utils.send_welcome_message(member)
        elif len(member.roles) > 3:
            if member_old.pending and not member.pending:
                if not utils.spammer_kicker(member):
                    await utils.send_welcome_message(member)


def setup(bot):
    bot.add_cog(MemberEvents(bot))
