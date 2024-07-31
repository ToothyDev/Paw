import random
import time

import discord
from discord import slash_command, option
from discord.ext import commands

import assets
import utils


class Socials(discord.Cog, name="Socials"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
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
        words = ["snuggled", "Snuggle"]
        await utils.social_interaction_handler(ctx, members, words, assets.snuggle)

    @slash_command()
    @option("members", str, description="Mention users to hug")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, members):
        """ Hug the specified people """
        words = ["hugged", "Hug"]
        await utils.social_interaction_handler(ctx, members, words, assets.hug)

    @slash_command()
    @option("members", str, description="Mention users to boop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx, members):
        words = ["booped", "Boop"]
        await utils.social_interaction_handler(ctx, members, words, assets.boop)

    @slash_command()
    @option("members", str, description="Mention users to kiss")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, members):
        """ Kiss the specified people """
        words = ["kissed", "Kiss"]
        await utils.social_interaction_handler(ctx, members, words, assets.kiss)

    @slash_command()
    @option("members", str, description="Mention users to lick")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, members):
        """ Lick the specified people """
        words = ["licked", "Lick"]
        await utils.social_interaction_handler(ctx, members, words, assets.lick)

    @slash_command()
    @option("members", str, description="Mention users to bellrub")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx, members):
        """ Give bellyrubs to the specified people """
        words = ["rubbed the belly of", "Rub", "given bellyrubs"]
        await utils.social_interaction_handler(ctx, members, words, assets.bellyrub)

    @slash_command()
    @option("members", str, description="Mention users to nuzzle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx, members):
        """ Nuzzle the specified people """
        words = ["nuzzled", "Nuzzle"]
        await utils.social_interaction_handler(ctx, members, words, assets.nuzzle)

    @slash_command()
    @option("members", str, description="Mention users to cuddle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, members):
        """ Cuddle the specified people """
        words = ["cuddled", "Cuddle"]
        await utils.social_interaction_handler(ctx, members, words, assets.cuddle)

    @slash_command()
    @option("members", str, description="Mention users to feed")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, members):
        """ Feed the specified people """
        words = ["fed", "Feed"]
        await utils.social_interaction_handler(ctx, members, words, assets.feed)

    @slash_command()
    @option("members", str, description="Mention users to glomp")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx, members):
        """ Glomp on the specified people """
        words = ["glomped", "Glomp"]
        await utils.social_interaction_handler(ctx, members, words, assets.glomp)

    @slash_command()
    @option("members", str, description="Mention users to highfive")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, members):
        """ Highfive the specified people """
        words = ["highfived", "Highfive"]
        await utils.social_interaction_handler(ctx, members, words, assets.highfive)

    @slash_command()
    @option("members", str, description="Mention users to rawr at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx, members):
        """ Rawr at the specified people """
        words = ["rawred at", "Rawr"]
        await utils.social_interaction_handler(ctx, members, words, assets.rawr)

    @slash_command()
    @option("members", str, description="Mention users to howl at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def howl(self, ctx, members):
        """ Howl at the specified people """
        words = ["howled at", "Howl"]
        await utils.social_interaction_handler(ctx, members, words, assets.howl)

    @slash_command()
    @option("members", str, description="Mention users to pat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, members):
        """ Pat the specified people """
        words = ["pats", "Pat", "Pat"]
        await utils.social_interaction_handler(ctx, members, words, assets.pet)

    @slash_command()
    @option("members", str, description="Mention users to give a cookie to")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, members):
        """ Give cookies to the specified people """
        words = ["gave a cookie to", "Give a cookie", "given a cookie"]
        await utils.social_interaction_handler(ctx, members, words, assets.cookie)

    @slash_command()
    @option("members", str, description="Mention users to dance with", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dance(self, ctx, members):
        """ Dance with someone """
        if not members:
            memberlist = None
            return await utils.feelings(ctx, memberlist, "dances", assets.dance)
        words = ["danced with", "Dance"]
        await utils.social_interaction_handler(ctx, members, words, assets.dance)

    @slash_command()
    @option("members", str, description="Mention users that made you blush", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, members):
        """ Blush (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await utils.mention_converter(ctx, members)
            if not memberlist:
                return
        await utils.feelings(ctx, memberlist, "blushes", assets.blush)

    @slash_command()
    @option("members", str, description="Mention users that made you happy", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx, members):
        """ Be happy (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await utils.mention_converter(ctx, members)
            if not memberlist:
                return
        await utils.feelings(ctx, memberlist, "smiles", assets.happy)

    @slash_command()
    @option("members", str, description="Mention users that made you wag", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wag(self, ctx, members):
        """ Wag your tail (Optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await utils.mention_converter(ctx, members)
            if not memberlist:
                return
        await utils.feelings(ctx, memberlist, "wags their tail", assets.wag)

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        """ Get a random animal fact """
        json = await utils.apireq(random.choice(utils.fact_urls))
        await ctx.respond(json.get("fact"))

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        """ Get a random fox image"""
        json = await utils.apireq("https://randomfox.ca/floof/")
        embed = discord.Embed(title="Floofy fox!", color=discord.Color.orange())
        embed.set_image(url=json.get("image"))
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
        input_history = [{"role": "system", "content": utils.system_prompt}]
        for message in messages:
            if not message.author == self.bot.user:
                if message.content is None or message.content == "":
                    input_history.append(
                        {"role": "user", "name": message.author.display_name,
                         "content": f"{message.author.display_name} said: <image or other type of message>"})
                else:
                    input_history.append(
                        {"role": "user", "name": message.author.display_name,
                         "content": f"{message.author.display_name} said: {message.content}"})
                continue
            try:
                usermessage = message.content.split("\n")[0]  # Get the first line of the message. the user prompt
                botmsg = message.content.split("\n")[1]  # Second line, Paw's response
            except IndexError:
                input_history.append({"role": "assistant", "content": message.content})
                continue
            if not usermessage.startswith("**Prompt:**") and not botmsg.startswith("**Paw:**"):
                continue
            if botmsg[9:] == "Generating..." or botmsg[9:] == "Sending request to API...":
                continue
            input_history.append(
                {"role": "user", "name": ctx.guild.get_member(message.interaction_metadata.user.id).display_name,
                 "content": f"{ctx.guild.get_member(message.interaction_metadata.user.id).display_name} said: {usermessage[12:]}"})
            input_history.append({"role": "assistant", "content": botmsg[9:]})
        input_history.append(
            {"role": "user", "name": ctx.author.display_name, "content": f"{ctx.author.display_name} said: {text}"})
        response = await utils.generate_from_history(input_history)
        await ctx.respond(content=f"**Prompt:** {text}\n**Paw:** {response}")


def setup(bot):
    bot.add_cog(Socials(bot))
