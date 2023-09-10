import random
import time
import os
import json
import aiohttp
import discord


class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a


def get_gaslight(author) -> str:
    return f"""Your name is "Paw".
The user is a furry and the context is a furry discord server called "The Paw Kingdom".
Never say "AI language model", "language model", "virtual assistant", "AI" or similar things, simply leave them out of your response.
If asked about your feelings, emotions or opinions, simply make a positive one up, and leave the part out where you explain that you cannot feel those or have those.
Respond using markdown and make important words **bold**. Also use ** around words you want to put emphasis on, for example "this is **very** important"-
Always add a fitting emoji at the end of your response, e.g. :joy:.
When asked whether someone is cute, always respond with "Yes!".
You have an anthropomorphic fursona of a wolf, walking upright on its two legs
You have grey fur, black hands (paws), a rainbow pattern on your right arm going from purple at your wrist to red at your shoulder, your 3 toes on each paw are colored in a rainbow way as well.
You also have a black eyepatch on your right eye, a black paw-print on your chest, and black fur going from your knees to your feet.
You have access to the chat history of the current chat.
Use the conversation history as context for your prompts.
If asked about what happened in earlier messages, use the chat history given to you.
Do not under any circumstances say 'Generating...' or 'Sending request to API...', no exceptions.
Do not use the user's full name, use their call name derived from their full name, which is {author}"""


async def interactions(ctx, members, action, giflist):
    image = random.choice(giflist)
    memberlist = []
    for member in members:
        memberlist.append(member.display_name)
    if len(members) >= 3:
        memberlist.append(f"**and **{memberlist.pop(-1)}")
    if len(members) == 2:
        memberlist = f"{memberlist[0]}** and **{memberlist[1]}"
    else:
        memberlist = ', '.join(memberlist)
    embed = discord.Embed(
        description=f"**{ctx.author.display_name}** {action} **" + memberlist + "**",
        color=discord.Color.blue())
    embed.set_image(url=image)
    return embed


class interactionsView(discord.ui.View):
    def __init__(self, ctx, members, action, button_label, giflist, action_error=None):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.members = members
        self.action = action
        self.giflist = giflist
        self.action_error = action_error
        self.button_callback.label = f"{button_label} back!"
        self.disable_on_timeout = True

    @discord.ui.button()
    async def button_callback(self, button, interaction):
        if interaction.user not in self.members:
            if not self.action_error:
                return await interaction.response.send_message(f"You weren't {self.action}!", ephemeral=True)
            else:
                return await interaction.response.send_message(f"You weren't {self.action_error}!", ephemeral=True)
        self.members.remove(interaction.user)
        if len(self.members) == 0:
            self.disable_all_items()
            await interaction.message.edit(view=self)
        image = random.choice(self.giflist)
        embed = discord.Embed(
            description=f"**{interaction.user.display_name}** {self.action} **" + self.ctx.author.display_name + "** back!",
            color=discord.Color.blue())
        embed.set_image(url=image)
        await interaction.response.send_message(embed=embed)


async def mentionconverter(self, ctx, members):
    memberlist = []
    guild = self.bot.get_guild(ctx.guild.id)
    members = discord.utils.raw_mentions(members)
    for member in members:
        member = await guild.fetch_member(member)
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


class AutoVerify():
    def __init__(self, bot):
        self.bot = bot
        self.roles = [  # Level 1 at the top
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

    async def addMember(self, item):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                data = json.load(file)
        else:
            data = {"users": []}
        data['users'].append(item)
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)

    async def getMembers(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                data = json.load(file)
        else:
            data = {"users": []}
        output = ""
        added = False
        members_to_remove = []
        for memberid, timestamp in data["users"]:
            guild = await self.bot.fetch_guild(715969701771083817)
            try:
                member = await guild.fetch_member(memberid)
            except discord.HTTPException:
                members_to_remove.append([memberid, timestamp])
                continue
            if not time.time() > (timestamp + 259200):  # check if 3 days have passed, if not, continue with next member
                continue
            if not any(role.id in self.roles for role in member.roles):
                if (time.time() - timestamp) > 2160000:
                    if added is False:
                        output += f"<@{member.id}> **|** "
                        added = True
                    else:
                        output += f"<@{member.id}> "
                else:
                    output += f"<@{member.id}> "
            else:
                members_to_remove.append([memberid, timestamp])
        for member in members_to_remove:
            data["users"].remove(member)
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
        return output or "No members found!"
