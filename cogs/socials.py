import random
import time

import discord
from discord import slash_command, option
from discord.ext import commands

import ai_handler
import data
from utils import mention_converter, interactions, feelings, apireq, get_gaslight
from views import InteractionsView


class Socials(discord.Cog, name="social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "♥️"
        self.last_revived = 0

    @slash_command()
    @option("topic", str, description="The topic to revive chat with", required=False)
    async def chat_revival(self, ctx, topic):
        """ Revive the chat! """
        revival_role = ctx.guild.get_role(738356235841175594)
        if revival_role not in ctx.author.roles:
            return await ctx.respond("You need the chat revival role to revive the chat! Get it in <id:customize>",
                                     ephemeral=True)
        if time.time() - 7200 <= self.last_revived:
            return await ctx.respond("Chat was revived less than 2 hours ago!", ephemeral=True)
        self.last_revived = time.time()
        await ctx.respond(
            f"<@&738356235841175594>! {topic if topic else 'Talk about something interesting!'}",
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=[revival_role]))

    @slash_command()
    @option("members", str, description="Mention users to snuggle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snuggle(self, ctx, members):
        """ Snuggle the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "snuggled", data.snuggle)
        view = InteractionsView(ctx, memberlist, "snuggled", "Snuggle", data.snuggle)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to hug")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, members):
        """ Hug the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "hugged", data.hug)
        view = InteractionsView(ctx, memberlist, "hugged", "Hug", data.hug)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to boop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx, members):
        """ Boop the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "booped", data.boop)
        view = InteractionsView(ctx, memberlist, "booped", "Boop", data.boop)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to kiss")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, members):
        """ Kiss the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "kissed", data.kiss)
        view = InteractionsView(ctx, memberlist, "kissed", "Kiss", data.kiss)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to lick")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, members):
        """ Lick the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "licked", data.lick)
        view = InteractionsView(ctx, memberlist, "licked", "Lick", data.lick)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to bellrub")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx, members):
        """ Give bellyrubs to the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "rubbed the belly of", data.bellyrub)
        view = InteractionsView(ctx, memberlist, "rubbed the belly of", "Rub", data.bellyrub, "given bellyrubs")
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to nuzzle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx, members):
        """ Nuzzle the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "nuzzled", data.nuzzle)
        view = InteractionsView(ctx, memberlist, "nuzzled", "Nuzzle", data.nuzzle)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to cuddle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, members):
        """ Cuddle the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "cuddled", data.cuddle)
        view = InteractionsView(ctx, memberlist, "cuddled", "Cuddle", data.cuddle)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to feed")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, members):
        """ Feed the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "fed", data.feed)
        view = InteractionsView(ctx, memberlist, "fed", "Feed", data.feed)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to glomp")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx, members):
        """ Glomp on the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "glomped", data.glomp)
        view = InteractionsView(ctx, memberlist, "glomped", "Glomp", data.glomp)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to highfive")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, members):
        """ Highfive the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "highfived", data.highfive)
        view = InteractionsView(ctx, memberlist, "highfived", "Highfive", data.highfive)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to rawr at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx, members):
        """ Rawr at the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "rawred at", data.rawr)
        view = InteractionsView(ctx, memberlist, "rawred at", "Rawr", data.rawr)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to howl at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def howl(self, ctx, members):
        """ Howl at the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "howled at", data.howl)
        view = InteractionsView(ctx, memberlist, "howled at", "Howl", data.howl)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to pat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, members):
        """ Pat the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "pats", data.pet)
        view = InteractionsView(ctx, memberlist, "pats", "Pat", data.pet, "Pat")
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to give a cookie to")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, members):
        """ Give cookies to the specified people """
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "gave a cookie to", data.cookie)
        view = InteractionsView(ctx, memberlist, "gave a cookie to", "Give a cookie", data.cookie, "given a cookie")
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users to dance with", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dance(self, ctx, members=False):
        """ Dance with someone """
        if not members:
            memberlist = None
            return await feelings(ctx, memberlist, "dances", data.dance)
        memberlist = await mention_converter(self, ctx, members)
        embed = await interactions(ctx, memberlist, "danced with", data.dance)
        view = InteractionsView(ctx, memberlist, "danced with", "Dance", data.dance)
        await ctx.respond(embed=embed, view=view)

    @slash_command()
    @option("members", str, description="Mention users that made you blush", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, members):
        """ Blush (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mention_converter(self, ctx, members)
        await feelings(ctx, memberlist, "blushes", data.blush)

    @slash_command()
    @option("members", str, description="Mention users that made you happy", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx, members):
        """ Be happy (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mention_converter(self, ctx, members)
        await feelings(ctx, memberlist, "smiles", data.happy)

    @slash_command()
    @option("members", str, description="Mention users that made you wag", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wag(self, ctx, members):
        """ Wag your tail (Optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mention_converter(self, ctx, members)
        await feelings(ctx, memberlist, "wags their tail", data.wag)

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        """ Get a random animal fact """
        facts = random.choice(["https://some-random-api.com/facts/dog", "https://some-random-api.com/facts/cat", "https://some-random-api.com/facts/panda",
                               "https://some-random-api.com/facts/fox", "https://some-random-api.com/facts/bird", "https://some-random-api.com/facts/koala"])

        fact = await apireq(facts)
        await ctx.respond(fact['fact'])

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        """ Get a random fox image"""
        json_data = await apireq("https://randomfox.ca/floof/")
        embed = discord.Embed(title="Floofy fox!", color=discord.Color.orange())
        embed.set_image(url=json_data['image'])
        await ctx.respond(embed=embed)

    @slash_command()
    @option("user", discord.Member, description="Select a user", required=False)
    @option("border", bool, description="Make it a border?", required=False)
    @option("server_avatar", bool, description="Use their server avatar?", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user=None, border=False, server_avatar=True):
        """ Gay overlay on avatar """
        if not user:
            user = ctx.author
        url = user.display_avatar.url if server_avatar else user.avatar.url
        link = f"https://some-random-api.com/canvas/misc/lgbt/?avatar={url}" if border else f"https://some-random-api.com/canvas/gay/?avatar={url}"
        embed = discord.Embed(color=discord.Color.random())
        embed.set_image(url=link)
        embed.set_footer(text=f"Gay avatar: {user.display_name}")
        await ctx.respond(embed=embed)

    @slash_command()
    @option("text", str, description="What do you want to tell Paw?")
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def gpt(self, ctx: discord.ApplicationContext, text: str):
        """ Talk to Paw! """
        await ctx.defer()
        messages = await ctx.channel.history(limit=50).flatten()
        messages.reverse()
        input_history = [{"role": "system", "content": get_gaslight()}]
        for message in messages:
            if not message.author == self.bot.user:
                if message.content is None or message.content == "":
                    input_history.append(
                        {"role": "user", "name": message.author.display_name,
                         "content": "<image or other type of message>"})
                else:
                    input_history.append(
                        {"role": "user", "name": message.author.display_name, "content": message.content})
                continue
            try:
                usermessage = message.content.split("\n")[
                    0]  # Get the first line of the message and remove the "Prompt" part
                botmsg = message.content.split("\n")[1]  # Same thing but remove the "Paw" part
            except IndexError:
                input_history.append({"role": "assistant", "content": message.content})
                continue
            if not usermessage.startswith("**Prompt:**") and not botmsg.startswith("**Paw:**"):
                continue
            if botmsg[9:] == "Generating..." or botmsg[9:] == "Sending request to API...":
                continue
            input_history.append(
                {"role": "user", "name": ctx.guild.get_member(message.interaction.user.id).display_name,
                 "content": usermessage[12:]})
            input_history.append({"role": "assistant", "content": botmsg[9:]})
        input_history.append({"role": "user", "name": ctx.author.display_name, "content": text})
        try:
            response = await ai_handler.generate_from_history(input_history)
        except Exception as e:
            return await ctx.respond(f"Something went wrong! Error: {e}")
        await ctx.respond(content=f"**Prompt:** {text}\n**Paw:** {response}")


def setup(bot):
    bot.add_cog(Socials(bot))
