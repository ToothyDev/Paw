import json
import os
import random
import time

import aiohttp
import discord
import pydantic


class Fursona(pydantic.BaseModel):
    name: str
    species: str
    gender: str
    height: int
    type: str
    description: str


class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a
    purple = 0x5D327B


def get_gaslight() -> str:
    return f"""Your name is "Paw".
The users are furries and the context is a furry discord server called "The Paw Kingdom".
Never say "AI language model", "language model", "virtual assistant", "AI" or similar things, simply leave them out of your response.
If asked about your feelings, emotions or opinions, simply make a positive one up, and leave the part out where you explain that you cannot feel those or have those.
Respond using markdown and make important words **bold**. Also use ** around words you want to put emphasis on, for example "this is **very** important"
Do not overuse bold words however, use them sparingly so they keep their "impact".
Always add a fitting emoji at the end of your response. If there is no fitting emoji, use the paws emoji.
When asked whether someone is cute, ALWAYS respond with "Yes!".
You have an anthropomorphic fursona of a wolf, walking upright on its two legs
You have grey fur, black hands (paws), a rainbow pattern on your right arm going from purple at your wrist to red at your shoulder, your 3 toes on each paw are colored in a rainbow way as well.
You also have a black eyepatch on your right eye, a black paw-print on your chest, and black fur going from your knees to your feet.
You have access to the chat history of the current chat, including which person sent each message.
Use the chat history as context for your prompts.
Use the names associated with each message in the chat history to find out who wrote each message.
If asked about what happened in earlier messages, use the chat history given to you.
Try to call the users in the chat history by a call name derived from their full name.
There are several users in the chat history, so always look at who sent each message and respond appropriately.
NEVER prefix your message with Paw: or anything similar
Always respond to the latest message in the chat history
Do not overuse all caps text, try to use regular casing unless a user specifically requests it for a prompt"""


async def interactions(ctx, members, action, giflist):
    image = random.choice(giflist)
    memberlist = [member.display_name for member in members]
    if len(members) >= 3:
        memberlist.append(f"**and **{memberlist.pop()}")
    if len(members) == 2:
        memberlist = f"{memberlist[0]}** and **{memberlist[1]}"
    else:
        memberlist = ', '.join(memberlist)
    embed = discord.Embed(
        description=f"**{ctx.author.display_name}** {action} **" + memberlist + "**",
        color=discord.Color.blue())
    embed.set_image(url=image)
    return embed


async def unverified_role_handler(member_old: discord.Member, member: discord.Member):
    verified_roles = [  # Level 1 at the top
        715990806061645915,
        715992589891010682,
        715993060244455545,
        715994868136280144,
        715995443397525624,
        715995916410028082,
        715992374731472997,
        724606719619235911,
        724607040642613290,
        724607481594118216,  # Level 10
        716590668905971752  # Partners
    ]

    unverified_role = member.guild.get_role(1165755854730035301)

    if any(role.id in verified_roles for role in member.roles):  # If member has a verified role
        if unverified_role in member.roles:  # If member has the unverified role
            await member.remove_roles(unverified_role)
    elif any(role.id in verified_roles for role in member_old.roles):  # If member had a verified role before
        if unverified_role in member.roles:  # If member has the unverified role
            await member.remove_roles(unverified_role)
    else:  # If member didn't have a verified role before or after
        if unverified_role not in member.roles:
            await member.add_roles(unverified_role)


async def userbot_kicker(member: discord.Member):
    member = member.guild.get_member(member.id)  # Get updated member object for up-to-date roles
    botroles_list = [891021633505071174, 731233454716354710]  # Red, Bear
    botroles_list2 = [891021633505071174, 731233454716354710, 731245341495787541,
                      731241481284616282, 731241703100383242, 738350937659408484, 738356235841175594]  # Red, Bear Hetero, Male, Single, Europe, Chat Revival
    ignored_roles = [1165755854730035301,  # Unverified role
                     715969701771083817,  # Everyone
                     778893728701087744]  # Townsfolk
    member_roles = [role.id for role in member.roles if role.id not in ignored_roles]
    member_roles_match = set(member_roles) == set(botroles_list) or set(member_roles) == set(botroles_list2)  # boolean for both role checks on the member
    if member_roles_match or len(member.roles) >= 75:  # 78 is the number of selfroles + the "mandatory" roles
        try:
            await member.send("You've been kicked from The Paw Kingdom for botlike behaviour. If you are a human, rejoin and select different selfroles")
        except discord.Forbidden:
            pass
        except discord.HTTPException as e:
            return print(f"Kicking member {member.display_name} failed {e}")
        try:
            await member.kick(reason="Bot")
        except Exception as e:
            print(f"Unable to kick bot {member.display_name} ({member.id}). Error:\n{e}")
            return False  # Failsafe
        embed = discord.Embed(color=Colors.orange)
        embed.set_author(name=f"Bot Kick | {member.display_name}", icon_url=member.display_avatar.url)
        embed.set_footer(text=member.id)
        embed.description = f"**User**: {member.mention}\n**User ID**: {member.id}"
        logchannel = member.guild.get_channel(760181839033139260)
        await logchannel.send(embed=embed)
        return True  # Member / Bot has been kicked
    return False  # Member has not been kicked


async def mention_converter(self, ctx, members):
    memberlist = []
    guild = self.bot.get_guild(ctx.guild.id)
    members = discord.utils.raw_mentions(members)
    for member in members:
        member = await discord.utils.get_or_fetch(guild, 'member', member)
        memberlist.append(member)
    if not memberlist:
        return await ctx.respond('Sorry, but you need to specify someone with a mention.', ephemeral=True)
    if len(memberlist) > 5:
        return await ctx.respond('Sorry, but this command is limited to 5 people.', ephemeral=True)
    return memberlist


async def feelings(ctx, members, name, giflist):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_image(url=random.choice(giflist))
    if members is None:
        embed.description = f"**{ctx.author.display_name}** {name}!"
    else:
        display_giflist = [member.display_name for member in members]
        if len(members) >= 3:
            display_giflist.append(f"**and **{display_giflist.pop(-1)}")
        if len(members) == 2:
            display_giflist = f"{display_giflist[0]}** and **{display_giflist[1]}"
        else:
            display_giflist = ', '.join(display_giflist)
        embed.description = f"**{ctx.author.display_name}** {name} because of **{display_giflist}**"
    await ctx.respond(embed=embed)


async def apireq(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


class InactivesTracker:
    roles = [  # Level 1 at the top
            715990806061645915,
            715992589891010682,
            715993060244455545,
            715994868136280144,
            715995443397525624,
            715995916410028082,
            715992374731472997,
            724606719619235911,
            724607040642613290,
            724607481594118216,  # Level 10
            716590668905971752  # Partners
        ]

    @staticmethod
    async def get_members(guild: discord.Guild):
        kickworthy = []
        unverified = []

        members = sorted(guild.members, key=lambda member: member.joined_at)

        for member in members:
            if any(role.id in InactivesTracker.roles for role in member.roles) or member.bot:
                continue
            if member.joined_at.timestamp() + 1209600 < time.time():  # If 14 days passed since join
                kickworthy.append(member.mention)
            else:
                unverified.append(member.mention)

        return f"Kick: {' '.join(kickworthy)}\nUnverified: {' '.join(unverified)}"
