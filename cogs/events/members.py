import discord

import utils


class MemberEvents(discord.Cog, name="Member Events"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await utils.log_member_join(member)
        await member.add_roles(member.guild.get_role(778893728701087744))
        await utils.spammer_kicker(member)

    @discord.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await utils.log_member_leave(member)

    @discord.Cog.listener()
    async def on_member_update(self, member_old: discord.Member, member: discord.Member):
        if member.guild.id != 715969701771083817:
            return

        if member.bot:  # If member is an ACTUAL bot
            return

        if await utils.userbot_kicker(member):  # If member is a bot (95% accurate)
            return

        await utils.unverified_role_handler(member_old, member)

        if len(member_old.roles) <= 3 < len(member.roles):
            if member.pending:
                return
            await utils.send_welcome_message(self.bot, member)
        elif len(member.roles) > 3 and member_old.pending and not member.pending:
            await utils.send_welcome_message(self.bot, member)


def setup(bot):
    bot.add_cog(MemberEvents(bot))
