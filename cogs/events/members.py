import discord

import utils
from utils import Colors


class MemberEvents(discord.Cog, name="Member Events"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.public_flags.value & 1048576 == 1048576:
            try:
                await member.send(
                    "You've been kicked from The Paw Kingdom for being flagged as spammer.")
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                return print(f"Kicking member {member.display_name} failed {e}")
            try:
                await member.kick(reason="Spammer")
            except Exception as e:
                return print(f"Unable to kick bot {member.display_name} ({member.id}). Error:\n{e}")
            embed = discord.Embed(color=Colors.orange)
            embed.set_author(name=f"Spammer Kick | {member.display_name}", icon_url=member.display_avatar.url)
            embed.set_footer(text=member.id)
            embed.description = f"**User**: {member.mention}\n**User ID**: {member.id}"
            logchannel = member.guild.get_channel(760181839033139260)
            await logchannel.send(embed=embed)

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
            await utils.send_welcome_message(member)
        elif len(member.roles) > 3:
            if member_old.pending and not member.pending:
                await utils.send_welcome_message(member)


def setup(bot):
    bot.add_cog(MemberEvents(bot))
