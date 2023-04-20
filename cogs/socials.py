import discord

import data
from discord.ext import commands, bridge
from utils import *


class socials(commands.Cog, name="social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "♥️"

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Snuggle someone")
    async def snuggle(self, ctx, *, members: str):
        """ Snuggle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "snuggled", 'snuggle', data.snuggle)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Hug someone")
    async def hug(self, ctx, *, members: str):
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "hugged", 'hug', data.hug, 'hug')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Boop someone")
    async def boop(self, ctx, *, members: str):
        """ Boop the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "booped", 'boop', data.boop)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Smooch someone", aliases=["kiss"])
    async def smooch(self, ctx, *, members: str):
        """ Smooch the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "smooched", 'smooch', data.smooch)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Lick someone")
    async def lick(self, ctx, *, members: str):
        """ Lick the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "licked", 'lick', data.lick)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Give bellyrubs!")
    async def bellyrub(self, ctx, *, members: str):
        """ Give bellyrubs to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "bellyrubbed", 'rub the belly of', data.bellyrub)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Nuzzle someone")
    async def nuzzle(self, ctx, *, members: str):
        """ Nuzzle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "nuzzled", 'nuzzles', data.nuzzle)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Cuddle someone")
    async def cuddle(self, ctx, *, members: str):
        """ Cuddle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "cuddled", 'cuddle', data.cuddle)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Feed someone")
    async def feed(self, ctx, *, members: str):
        """ Feed the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "fed", 'feed', data.feed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Glomp someone")
    async def glomp(self, ctx, *, members: str):
        """ Glomp on the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "glomped", 'glomp', data.glomp)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Highfive someone")
    async def highfive(self, ctx, *, members: str):
        """ Highfive the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "highfived", 'hivefive', data.highfive)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Rawrrrr")
    async def rawr(self, ctx, *, members: str):
        """ Rawr at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "rawred at", 'rawr at', data.rawr)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Howl to the moon, or someone", aliases=["howl"])
    async def awoo(self, ctx, *, members: str):
        """ Howl at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "howled at", 'howl at', data.awoo)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="pat someone!", aliases=["pet"])
    async def pat(self, ctx, *, members: str):
        """ Pat the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "patted", 'pat', data.pet, 'pat')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Gib cookie")
    async def cookie(self, ctx, *, members: str):
        """ Give cookies to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "gave a cookie to", 'give a cookie to', data.cookie)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Blushies!")
    async def blush(self, ctx, *, members: str = "None"):
        """ Blush (optionally because of specified people) """
        if members == "None":
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "blushes", data.blush)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="Be happy")
    async def happy(self, ctx, *, members: str = "None"):
        """ Be happy (optionally because of specified people) """
        if members == "None":
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "smiles", data.happy)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @bridge.bridge_command(brief="wag yer tail")
    async def wag(self, ctx, *, members: str = "None"):
        """ Wag your tail (Optionally because of specified people) """
        if members == "None":
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "wags their tail", data.wag)

    @bridge.bridge_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        """ Get a random animal fact """
        facts = random.choice(["https://some-random-api.ml/facts/dog", "https://some-random-api.ml/facts/cat", "https://some-random-api.ml/facts/panda",
                               "https://some-random-api.ml/facts/fox", "https://some-random-api.ml/facts/bird", "https://some-random-api.ml/facts/koala"])

        async with aiohttp.ClientSession() as cs:
            async with cs.get(facts) as r:
                js = await r.json()

                await ctx.respond(js['fact'])

    @bridge.bridge_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        """ Get a random fox """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof/") as r:
                js = await r.json()

                e = discord.Embed(title="Floofy fox!", color=discord.Color.orange())
                e.set_image(url=js['image'])
                await ctx.respond(embed=e)

    @bridge.bridge_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None):
        """ Gay overlay on avatar """
        if not user:
            user = ctx.author
        link = f"https://some-random-api.ml/canvas/gay/?avatar={user.avatar.url}"
        e = discord.Embed(color=discord.Color.random())
        e.set_image(url=link)
        e.set_footer(text=f"Gay avatar: {user}")
        await ctx.respond(embed=e)


def setup(bot):
    bot.add_cog(socials(bot))
