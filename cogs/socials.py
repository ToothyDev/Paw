import gifs
from discord.ext import commands
from utils import *


class socials(commands.Cog, name="social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "♥️"

    @commands.command(brief="Snuggle someone")
    async def snuggle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Snuggle the specified people"""
        await interactions(ctx, members, "snuggled", 'snuggle', gifs.snuggle, reason)

    @commands.command(brief="Hug someone")
    async def hug(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        await interactions(ctx, members, "hugged", 'hug', gifs.hug, reason, 'hug')

    @commands.command(brief="Boop someone")
    async def boop(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Boop the specified people"""
        await interactions(ctx, members, "booped", 'boop', gifs.boop, reason)

    @commands.command(brief="Smooch someone", aliases=["kiss"])
    async def smooch(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Smooch the specified people"""
        await interactions(ctx, members, "smooched", 'smooch', gifs.smooch, reason)

    @commands.command(brief="Lick someone")
    async def lick(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Lick the specified people"""
        await interactions(ctx, members, "licked", 'lick', gifs.lick, reason)

    @commands.command(brief="Give bellyrubs!")
    async def bellyrub(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Give bellyrubs to the specified people"""
        await interactions(ctx, members, "bellyrubbed", 'rub the belly of', gifs.bellyrub, reason)

    @commands.command(brief="Nuzzle someone")
    async def nuzzle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Nuzzle the specified people"""
        await interactions(ctx, members, "nuzzled", 'nuzzles', gifs.nuzzle, reason)

    @commands.command(brief="Cuddle someone")
    async def cuddle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Cuddle the specified people"""
        await interactions(ctx, members, "cuddled", 'cuddle', gifs.cuddle, reason)

    @commands.command(brief="Feed someone")
    async def feed(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Feed the specified people"""
        await interactions(ctx, members, "fed", 'feed', gifs.feed, reason)

    @commands.command(brief="Glomp someone")
    async def glomp(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Glomp on the specified people"""
        await interactions(ctx, members, "glomped", 'glomp', gifs.glomp, reason)

    @commands.command(brief="Highfive someone")
    async def highfive(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Highfive the specified people"""
        await interactions(ctx, members, "highfived", 'hivefive', gifs.highfive, reason)

    @commands.command(brief="Rawrrrr")
    async def rawr(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Rawr at the specified people"""
        await interactions(ctx, members, "rawred at", 'rawr at', gifs.rawr, reason)

    @commands.command(brief="Howl to the moon, or someone", aliases=["howl"])
    async def awoo(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Howl at the specified people"""
        await interactions(ctx, members, "howled at", 'howl at', gifs.awoo)

    @commands.command(brief="pat someone!", aliases=["pet"])
    async def pat(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Pat the specified people"""
        await interactions(ctx, members, "patted", 'pat', gifs.pet, reason, 'pat')

    @commands.command(brief="Gib cookie")
    async def cookie(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Give cookies to the specified people"""
        await interactions(ctx, members, "gave a cookie to", 'give a cookie to', gifs.cookie, reason)

    @commands.command(brief="Blushies!")
    async def blush(self, ctx, members: commands.Greedy[discord.Member]):
        """Blush (optionally because of specified people)"""
        await feelings(ctx, members, "blushes", gifs.blush)

    @commands.command(brief="Be happy")
    async def happy(self, ctx, members: commands.Greedy[discord.Member]):
        """Be happy (optionally because of specified people)"""
        await feelings(ctx, members, "smiles", gifs.happy)

    @commands.command(brief="wag yer tail")
    async def wag(self, ctx, members: commands.Greedy[discord.Member]):
        """Wag your tail (Optionally because of specified people)"""
        await feelings(ctx, members, "wags their tail", gifs.wag)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        facts = random.choice(["https://some-random-api.ml/facts/dog", "https://some-random-api.ml/facts/cat", "https://some-random-api.ml/facts/panda",
                               "https://some-random-api.ml/facts/fox", "https://some-random-api.ml/facts/bird", "https://some-random-api.ml/facts/koala"])

        async with aiohttp.ClientSession() as cs:
            async with cs.get(facts) as r:
                js = await r.json()

                await ctx.send(js['fact'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        """ Get a random fox """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof/") as r:
                js = await r.json()

                e = discord.Embed(title="Floofy fox!", color=discord.Color.orange())
                e.set_image(url=js['image'])
                await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None):
        """ Gay overlay on avatar """
        if not user:
            user = ctx.author
        link = f"https://some-random-api.ml/canvas/gay/?avatar={user.avatar.url}"
        e = discord.Embed(color=discord.Color.random())
        e.set_image(url=link)
        e.set_footer(text=f"Gay avatar: {user}")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(socials(bot))
