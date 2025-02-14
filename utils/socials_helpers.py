import base64
import random

import discord

import config
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


async def mention_converter(ctx: discord.ApplicationContext, members: str) -> list[discord.Member] | None:
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


async def social_interaction_handler(ctx: discord.ApplicationContext, members: str, words: list[str],
                                     gifs: list[str]):
    memberlist = await mention_converter(ctx, members)
    if not memberlist:
        return
    embed = await interactions(ctx, memberlist, words[0], gifs)
    view = InteractionsView(ctx, memberlist, words[0], words[1], gifs, words[2] if len(words) > 2 else None)
    await ctx.respond(embed=embed, view=view)


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
            "name": user.display_name if user else message.interaction_metadata.user.global_name,
            "content": f"{user.display_name if user else message.interaction_metadata.user.global_name} ({utils.get_gender(user) if user else ""}) said: {user_prompt.removeprefix('**Prompt:** ')}"
        },
        {"role": "assistant", "content": bot_response.removeprefix('**Paw:** ')}
    ]


async def _format_user_message(message: discord.Message) -> dict:
    if config.omni_model:  # If the model can handle text and images
        return await _parse_message_with_image(message)
    else:  # Legacy approach for non-multimodal models / if two different models are used
        alt_text = await _get_image_alt_text(message)
        content = message.clean_content if message.content else f"{message.author.display_name} sent a file."
        return {
            "role": "user",
            "name": message.author.display_name,
            "content": f"{message.author.display_name} ({utils.get_gender(message.author)}) said: {content}{alt_text}"
        }


async def _parse_message_with_image(message: discord.Message) -> dict:
    """ Handles the new approach for multimodal models by directly inserting the image into the message history """
    text_content = f"{message.author.display_name} ({utils.get_gender(message.author)}) said: {message.clean_content}"
    image_attachments = [a for a in message.attachments if a.content_type.startswith("image")]

    if not image_attachments:
        return {
            "role": "user",
            "name": message.author.display_name,
            "content": text_content
        }

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
        "name": message.author.display_name,
        "content": content,
    }


def _format_current_user_message(author: discord.Member, text: str) -> dict:
    return {
        "role": "user",
        "name": author.display_name,
        "content": f"{author.display_name} ({utils.get_gender(author)}) said: {text}"
    }


async def _get_image_alt_text(message: discord.Message) -> str:
    if not message.attachments:
        return ""

    if len([attachment for attachment in message.attachments if attachment.content_type.startswith("image")]) == 0:
        return ""

    if len(message.attachments) == 1 and message.attachments[0].content_type.startswith("image"):
        return f"\nThe user attached an image to the message which shows the following: {await utils.analyse_image(await message.attachments[0].read())}"

    output = "\nThe user attached multiple images to the message which show the following: "
    # This is for groq compatibility; OpenAI and Gemini can take multiple images per message easily
    for attachment in message.attachments:
        if attachment.content_type.startswith("image"):
            output += "\n" + await utils.analyse_image(await attachment.read())
    return output
