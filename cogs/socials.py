import data
from discord.ext import commands, bridge
from utils import *
import aiohttp


class socials(commands.Cog, name="social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "♥️"

    @bridge.bridge_command(brief="Snuggle someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snuggle(self, ctx, *, members: str):
        """ Snuggle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "snuggled", 'snuggle', data.snuggle)

    @bridge.bridge_command(brief="Hug someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, *, members: str):
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "hugged", 'hug', data.hug, 'Hug')

    @bridge.bridge_command(brief="Boop someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx, *, members: str):
        """ Boop the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "booped", 'boop', data.boop)

    @bridge.bridge_command(brief="Smooch someone", aliases=["kiss"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smooch(self, ctx, *, members: str):
        """ Smooch the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "smooched", 'smooch', data.smooch)

    @bridge.bridge_command(brief="Lick someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, *, members: str):
        """ Lick the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "licked", 'lick', data.lick)

    @bridge.bridge_command(brief="Give bellyrubs!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx, *, members: str):
        """ Give bellyrubs to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "bellyrubbed", 'rub the belly of', data.bellyrub, "Rub")

    @bridge.bridge_command(brief="Nuzzle someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx, *, members: str):
        """ Nuzzle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "nuzzled", 'nuzzles', data.nuzzle)

    @bridge.bridge_command(brief="Cuddle someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, *, members: str):
        """ Cuddle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "cuddled", 'cuddle', data.cuddle)

    @bridge.bridge_command(brief="Feed someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, *, members: str):
        """ Feed the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "fed", 'feed', data.feed)

    @bridge.bridge_command(brief="Glomp someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx, *, members: str):
        """ Glomp on the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "glomped", 'glomp', data.glomp)

    @bridge.bridge_command(brief="Highfive someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, *, members: str):
        """ Highfive the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "highfived", 'highfive', data.highfive)

    @bridge.bridge_command(brief="Rawrrrr")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx, *, members: str):
        """ Rawr at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "rawred at", 'rawr at', data.rawr, "Rawr")

    @bridge.bridge_command(brief="Howl to the moon, or someone", aliases=["howl"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def awoo(self, ctx, *, members: str):
        """ Howl at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "howled at", 'howl at', data.awoo, "Howl")

    @bridge.bridge_command(brief="pat someone!", aliases=["pet"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, *, members: str):
        """ Pat the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "pats", 'pat', data.pet, 'Pat')

    @bridge.bridge_command(brief="Gib cookie")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, *, members: str):
        """ Give cookies to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "gave a cookie to", 'give a cookie to', data.cookie, "Give a cookie")

    @bridge.bridge_command(brief="Dance with someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dance(self, ctx, *, members: str = None):
        """ Dance with someone """
        if not members:
            memberlist = None
            return await feelings(ctx, memberlist, "dances", data.dance)
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "danced with", "dance with", data.dance, "Dance")

    @bridge.bridge_command(brief="Blushies!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, *, members: str = "None"):
        """ Blush (optionally because of specified people) """
        if members == "None":
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "blushes", data.blush)

    @bridge.bridge_command(brief="Be happy")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx, *, members: str = "None"):
        """ Be happy (optionally because of specified people) """
        if members == "None":
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "smiles", data.happy)

    @bridge.bridge_command(brief="wag yer tail")
    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @bridge.bridge_command(options=[
        discord.Option(discord.Member, name="user", description="Select a user"),
        discord.Option(bool, name="border", description="Make it a border?", required=False),
        discord.Option(bool, name="server-avatar", description="Use their server avatar?", required=False)
    ])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None, border: bool = False, server_avatar: bool = False):
        """ Gay overlay on avatar """
        link = ""
        if not user:
            if ctx.message:  # additional check to make slash commands not break at .message.reference
                if ctx.message.reference:
                    reference = await ctx.fetch_message(ctx.message.reference.message_id)
                    user = reference.author
            else:
                user = ctx.author
        if not server_avatar:
            url = user.avatar.url
        else:
            url = user.display_avatar.url
        if not border:
            link = f"https://some-random-api.ml/canvas/gay/?avatar={url}"
        else:
            link = f"https://some-random-api.ml/canvas/misc/lgbt/?avatar={url}"
        e = discord.Embed(color=discord.Color.random())
        e.set_image(url=link)
        e.set_footer(text=f"Gay avatar: {user}")
        await ctx.respond(embed=e)


def setup(bot):
    bot.add_cog(socials(bot))
