import random

import discord

import utils
from views import InteractionsView


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


async def mention_converter(ctx: discord.ApplicationContext, members) -> list[discord.Member] | None:
    memberlist = []
    guild = ctx.guild
    members = discord.utils.raw_mentions(members)
    for member in members:
        member = await discord.utils.get_or_fetch(guild, 'member', member)
        memberlist.append(member)
    if not memberlist:
        await ctx.respond('Sorry, but you need to specify someone with a mention.', ephemeral=True)
        return None
    if len(memberlist) > 5:
        await ctx.respond('Sorry, but this command is limited to 5 people.', ephemeral=True)
        return None
    return memberlist


async def social_interaction_handler(ctx: discord.ApplicationContext, members: list[str], words: list[str],
                                     gifs: list[str]):
    memberlist = await mention_converter(ctx, members)
    if not memberlist:
        return
    embed = await interactions(ctx, memberlist, words[0], gifs)
    view = InteractionsView(ctx, memberlist, words[0], words[1], gifs, words[2] if len(words) > 2 else None)
    await ctx.respond(embed=embed, view=view)


def format_current_user_message(author: discord.Member, text: str) -> dict:
    return {
        "role": "user",
        "name": author.display_name,
        "content": f"{author.display_name} ({utils.get_gender(author)}) said: {text}"
    }


def format_bot_message(message: discord.Message, guild: discord.Guild) -> list:
    try:
        user_prompt, bot_response = message.content.split("\n", 1)
    except ValueError:
        return [{"role": "assistant", "content": message.content}]

    if not user_prompt.startswith("**Prompt:**") or not bot_response.startswith("**Paw:**"):
        return []

    user = guild.get_member(message.interaction_metadata.user.id)
    return [
        {
            "role": "user",
            "name": user.display_name,
            "content": f"{user.display_name} ({utils.get_gender(user)}) said: {user_prompt[12:]}"
        },
        {"role": "assistant", "content": bot_response[9:]}
    ]


async def get_image_alt_text(message: discord.Message) -> str:
    if message.attachments and message.attachments[0].content_type.startswith("image"):
        return f"\nThe user attached an image to the message: {await utils.analyse_image(message.attachments[0].url)}"
    return ""


async def format_user_message(message: discord.Message) -> dict:
    alt_text = await get_image_alt_text(message)
    content = message.content if message.content else f"{message.author.display_name} sent a file."
    return {
        "role": "user",
        "name": message.author.display_name,
        "content": f"{message.author.display_name} ({utils.get_gender(message.author)}) said: {content} {alt_text}"
    }


async def get_channel_history(channel) -> list[discord.Message]:
    messages = await channel.history(limit=50).flatten()
    messages.reverse()
    return messages


async def build_input_history(bot, ctx: discord.ApplicationContext, prompt: str) -> list:
    messages = await get_channel_history(ctx.channel)
    input_history = [{"role": "system", "content": utils.SYSTEM_PROMPT}]

    for message in messages:
        if message.author != bot.user:
            input_history.append(await format_user_message(message))
        else:
            input_history.extend(format_bot_message(message, ctx.guild))

    input_history.append(format_current_user_message(ctx.author, prompt))
    return input_history
