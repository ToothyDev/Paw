import random
import discord
import aiohttp
from discord.ext import tasks
import time


class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a


async def interactions(ctx, members, action, giflist):
    image = random.choice(giflist)
    memberlist = []
    for member in members:
        memberlist.append(member.display_name)
    if len(members) >= 3:
        memberlist.append(f"and {memberlist.pop(-1)}")
    if len(members) == 2:
        memberlist = f"{memberlist[0]} and {memberlist[1]}"
    else:
        memberlist = ', '.join(memberlist)
    embed = discord.Embed(
        description=f"**{ctx.author.display_name}** {action} **" + memberlist + "**",
        color=discord.Color.blue())
    embed.set_thumbnail(url=image)
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
            description=f"**{interaction.user.name}** {self.action} **" + self.ctx.author.name + "** back!",
            color=discord.Color.blue())
        embed.set_thumbnail(url=image)
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
    embed.set_thumbnail(url=random.choice(giflist))
    if members is None:
        embed.description = f"**{ctx.author.display_name}** {name}!"
    else:
        display_giflist = []
        for x in members:
            display_giflist.append(x.display_name)
        if len(members) >= 3:
            display_giflist.append(f"**and **{display_giflist.pop(-1)}")
        if len(members) == 2:
            display_giflist = f"{display_giflist[0]}** and **{display_giflist[1]}"
        else:
            display_giflist = ', '.join(display_giflist)
        embed.description = f"**{ctx.author.display_name}** {name} because of **{display_giflist}**"
    await ctx.respond(embed=embed)


async def apireq(url):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            js = await r.json()
            return js


class AutoVerify():
    def __init__(self, bot):
        self.bot = bot
        self.members = []
        self.roles = [
            866064455183892509
        ]
        self.memberkicker.start()

    @tasks.loop(seconds=20)
    async def memberkicker(self):
        for memberid, guildid, timestamp in self.members:
            guild = await self.bot.fetch_guild(guildid)
            member = await guild.fetch_member(memberid)
            if time.time() > (timestamp + 1):
                print("Time's up, boye!")
                for role in member.roles:
                    if role.id not in self.roles:
                        await member.kick(reason="Didn't verify")
                    self.members.remove((memberid, guildid, timestamp))

    def addMember(self, item):
        self.members.append(item)
