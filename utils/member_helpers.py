import time

import discord

import logger
import utils

log = logger.get_logger(__name__)


async def send_welcome_message(bot: discord.Bot, member: discord.Member):
    channel = member.guild.get_channel(1066357407443333190)
    accent = (await bot.fetch_user(member.id)).accent_color

    components = [
        discord.ui.Container(
            discord.ui.Section(
                discord.ui.TextDisplay(f"""### <@&822886791312703518>, welcome {member.mention} to the server!"""),
                discord.ui.TextDisplay("""
    Feel free to visit <id:customize> for roles & channels and <id:guide> for some useful info about the server!
    __**IMPORTANT**__: To verify yourself, you first need to gain a level by chatting, else you will be kicked for inactivity. Thank you for reading and have fun!"""),
                accessory=discord.ui.Thumbnail(url=member.display_avatar.url)
            ),
            color=accent
        )
    ]

    await channel.send(view=discord.ui.View(*components))


async def unverified_role_handler(member_old: discord.Member, member: discord.Member):
    verified_roles = utils.INACTIVE_ROLES

    unverified_role = member.guild.get_role(1165755854730035301)

    if any(role.id in verified_roles for role in member.roles) or any(
            role.id in verified_roles for role in member_old.roles):  # If member has a verified role or had one before
        if unverified_role in member.roles:  # If member has the unverified role
            await member.remove_roles(unverified_role)
    else:  # If member didn't have a verified role before or after
        if unverified_role not in member.roles:
            await member.add_roles(unverified_role)


async def userbot_kicker(member: discord.Member):
    member = member.guild.get_member(member.id)  # Get updated member object for up-to-date roles
    botroles_list = [891021633505071174, 731233454716354710]  # Red, Bear
    botroles_list2 = [891021633505071174, 731233454716354710, 731245341495787541,
                      731241481284616282, 731241703100383242, 738350937659408484,
                      738356235841175594]  # Red, Bear Hetero, Male, Single, Europe, Chat Revival
    ignored_roles = [1165755854730035301,  # Unverified role
                     715969701771083817,  # Everyone
                     778893728701087744]  # Townsfolk
    member_roles = [role.id for role in member.roles if role.id not in ignored_roles]
    member_roles_match = set(member_roles) == set(botroles_list) or set(member_roles) == set(
        botroles_list2)  # boolean for both role checks on the member
    if member_roles_match or len(member.roles) >= 75:  # 78 is the number of selfroles + the "mandatory" roles
        try:
            await member.send(
                "You've been kicked from The Paw Kingdom for botlike behaviour. If you are a human, rejoin and select "
                "different selfroles")
        except (discord.HTTPException, discord.Forbidden):
            pass
        try:
            await member.kick(reason="Bot")
        except (discord.HTTPException, discord.Forbidden) as e:
            log.warning(f"Unable to kick bot {member.display_name} ({member.id}). Error:\n{e}")
            return False  # Failsafe
        await log_member_kick(member, "Bot")
        return True  # Member / Bot has been kicked
    return False  # Member has not been kicked


async def spammer_kicker(member: discord.Member) -> bool:
    if not member.public_flags.value & 1 << 20:
        return False  # Member is not a spammer

    try:
        await member.send(
            "You've been kicked from The Paw Kingdom for being flagged as spammer. If you think this is a "
            "mistake, send a friend request to `toothyfernsan`")
    except (discord.HTTPException, discord.Forbidden):
        pass
    try:
        await member.kick(reason="Spammer")
    except (discord.HTTPException, discord.Forbidden) as e:
        log.warning(f"Unable to kick spammer {member.display_name} ({member.id}). Error:\n{e}")
        return False  # Member is a spammer, tho failsafe because it failed
    await log_member_kick(member, "Spammer")
    return True  # Member has been detected as spammer


async def log_member_kick(member: discord.Member, member_class: str):
    embed = discord.Embed(color=utils.Colors.ORANGE)
    embed.set_author(name=f"{member_class} Kick | {member.display_name}", icon_url=member.display_avatar.url)
    embed.description = f"**User**: {member.mention}\n**User ID**: {member.id}"
    logchannel = member.guild.get_channel(760181839033139260)
    await logchannel.send(embed=embed)


def get_inactives(guild: discord.Guild) -> dict[str, list[discord.Member]]:
    unverified = []
    kickworthy = []
    current_time = time.time()
    for member in guild.members:
        if any(role.id in utils.INACTIVE_ROLES for role in member.roles) or member.bot:
            continue
        if member.joined_at.timestamp() + 604800 < current_time:  # If 7 days passed since join
            kickworthy.append(member)
        else:
            unverified.append(member)

    return {"unverified": unverified, "kickworthy": kickworthy}


def get_gender(member: discord.Member) -> str:
    if isinstance(member, discord.User) or member.guild.id != 715969701771083817:
        return "undetermined gender"

    male_role = member.guild.get_role(731241481284616282)
    female_role = member.guild.get_role(731241521558323227)

    if male_role in member.roles and female_role not in member.roles:
        return "Male"
    elif female_role in member.roles and male_role not in member.roles:
        return "Female"
    else:
        return "undetermined gender"
