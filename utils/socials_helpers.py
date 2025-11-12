import base64
import random

import discord

import utils
from views import InteractionsView


async def feelings(ctx, members, name, giflist):
    if members is None:
        view_text = f"**{ctx.author.mention}** {name}!"
    else:
        member_mentions = [member.mention for member in members]
        if len(members) >= 3:
            member_mentions.append(f"**and **{member_mentions.pop(-1)}")
        if len(members) == 2:
            member_mentions = f"{member_mentions[0]}** and **{member_mentions[1]}"
        else:
            member_mentions = ', '.join(member_mentions)
        view_text = f"**{ctx.author.display_name}** {name} because of **{member_mentions}**"

    components = [
        discord.ui.Container(
            discord.ui.TextDisplay(view_text),
            discord.ui.MediaGallery(discord.MediaGalleryItem(url=random.choice(giflist))),
            color=discord.Color.blue()
        )
    ]

    await ctx.respond(view=discord.ui.DesignerView(*components))


async def mention_converter(ctx: discord.ApplicationContext, members: str) -> list[discord.Member] | None:
    memberlist = []
    guild = ctx.guild
    members = discord.utils.raw_mentions(members)
    for member in members:
        member = await discord.utils.get_or_fetch(guild, discord.Member, member)
        memberlist.append(member)
    if not memberlist:
        await ctx.respond('Sorry, but you need to specify someone with a mention.', ephemeral=True)
        return None
    if len(memberlist) > 5:
        await ctx.respond('Sorry, but this command is limited to 5 people.', ephemeral=True)
        return None
    return memberlist


async def social_interaction_handler(ctx: discord.ApplicationContext, members: str, words: list[str],
                                     gifs: list[str]):
    memberlist = await mention_converter(ctx, members)
    if not memberlist:
        return
    view = InteractionsView(ctx, memberlist, words[0], words[1], gifs, words[2] if len(words) > 2 else None)
    await ctx.respond(view=view, allowed_mentions=discord.AllowedMentions(users=memberlist))


async def build_input_history(bot, channel: discord.TextChannel, author: discord.Member, guild: discord.Guild,
                              prompt: str) -> list:
    messages = await channel.history(
        limit=26).flatten()  # Get actual-limit + 1 messsage (the defer, or user message if invoked via mention)
    messages.reverse()
    input_history = [{"role": "system", "content": utils.SYSTEM_PROMPT}]

    for message in messages:
        if message.author == bot.user:
            input_history.extend(_format_bot_message(message, guild))
        else:
            input_history.append(await _format_user_message(message))

    input_history = input_history[:-1]  # Cut the defer message (the most recent one) from the history
    input_history.append(_format_current_user_message(author, prompt))
    return input_history


def _format_bot_message(message: discord.Message, guild: discord.Guild) -> list[dict]:
    try:
        user_prompt, bot_response = message.clean_content.split("\n", 1)
    except ValueError:
        return [
            {"role": "assistant", "content": message.clean_content if message.clean_content else "<no message body>"}]

    if not user_prompt.startswith("**Prompt:**") or not bot_response.startswith("**Paw:**"):
        return []

    user = guild.get_member(message.interaction_metadata.user.id)

    return [
        {
            "role": "user",
            "name": f"{user.display_name if user else message.interaction_metadata.user.global_name} ({utils.get_gender(user) if user else ""})",
            "content": f"{user.display_name if user else message.interaction_metadata.user.global_name} ({utils.get_gender(user) if user else ""}) said: {user_prompt.removeprefix('**Prompt:** ')}"
        },
        {"role": "assistant", "content": bot_response.removeprefix('**Paw:** ')}
    ]


async def _format_user_message(message: discord.Message) -> dict:
    text_content = f"{message.author.display_name} ({utils.get_gender(message.author)}) said: {message.clean_content}"
    image_attachments = [a for a in message.attachments if a.content_type.startswith("image")]

    content = [{"type": "text", "text": text_content}]
    for attachment in image_attachments:
        image_data = await attachment.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}",
            },
        })

    return {
        "role": "user",
        "name": f"{message.author.display_name} ({utils.get_gender(message.author)})",
        "content": content,
    }


def _format_current_user_message(author: discord.Member, text: str) -> dict:
    return {
        "role": "user",
        "name": f"{author.display_name} ({utils.get_gender(author)})",
        "content": f"{author.display_name} ({utils.get_gender(author)}) said: {text}"
    }
