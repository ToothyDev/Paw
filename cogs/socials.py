import data
from discord.ext import commands, bridge
from discord import slash_command, option
from utils import *
import aiohttp


class socials(commands.Cog, name="social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "♥️"

    @bridge.bridge_command(brief="Snuggle someone")
    @option("members", str, description="Mention users to snuggle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snuggle(self, ctx, *, members):
        """ Snuggle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "snuggled", 'snuggle', data.snuggle)

    @bridge.bridge_command(brief="Hug someone")
    @option("members", str, description="Mention users to hug")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, *, members):
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "hugged", 'hug', data.hug, 'Hug')

    @bridge.bridge_command(brief="Boop someone")
    @option("members", str, description="Mention users to boop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx, *, members):
        """ Boop the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "booped", 'boop', data.boop)

    @bridge.bridge_command(brief="Kiss someone")
    @option("members", str, description="Mention users to kiss")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smooch(self, ctx, *, members):
        """ Smooch the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "smooched", 'smooch', data.smooch)

    @bridge.bridge_command(brief="Lick someone")
    @option("members", str, description="Mention users to lick")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, *, members):
        """ Lick the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "licked", 'lick', data.lick)

    @bridge.bridge_command(brief="Give someone bellyrubs")
    @option("members", str, description="Mention users to bellrub")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx, *, members):
        """ Give bellyrubs to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "bellyrubbed", 'rub the belly of', data.bellyrub, "Rub")

    @bridge.bridge_command(brief="Nuzzle someone")
    @option("members", str, description="Mention users to nuzzle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx, *, members):
        """ Nuzzle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "nuzzled", 'nuzzles', data.nuzzle)

    @bridge.bridge_command(brief="Cuddle someone")
    @option("members", str, description="Mention users to cuddle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, *, members):
        """ Cuddle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "cuddled", 'cuddle', data.cuddle)

    @bridge.bridge_command(brief="Feed someone")
    @option("members", str, description="Mention users to feed")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, *, members):
        """ Feed the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "fed", 'feed', data.feed)

    @bridge.bridge_command(brief="Glomp someone")
    @option("members", str, description="Mention users to glomp")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx, *, members):
        """ Glomp on the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "glomped", 'glomp', data.glomp)

    @bridge.bridge_command(brief="Highfive someone")
    @option("members", str, description="Mention users to highfive")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, *, members):
        """ Highfive the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "highfived", 'highfive', data.highfive)

    @bridge.bridge_command(brief="Rawr")
    @option("members", str, description="Mention users to rawr at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx, *, members):
        """ Rawr at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "rawred at", 'rawr at', data.rawr, "Rawr")

    @bridge.bridge_command(brief="Howl to the moon, or someone")
    @option("members", str, description="Mention users to howl at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def howl(self, ctx, *, members):
        """ Howl at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "howled at", 'howl at', data.awoo, "Howl")

    @bridge.bridge_command(brief="Pat someone")
    @option("members", str, description="Mention users to pat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, *, members):
        """ Pat the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "pats", 'pat', data.pet, 'Pat')

    @bridge.bridge_command(brief="Give a cookie to someone")
    @option("members", str, description="Mention users to give a cookie to")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, *, members):
        """ Give cookies to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "gave a cookie to", 'give a cookie to', data.cookie, "Give a cookie")

    @bridge.bridge_command(brief="Dance with someone")
    @option("members", str, description="Mention users to dance with", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dance(self, ctx, *, members=False):
        """ Dance with someone """
        if not members:
            memberlist = None
            return await feelings(ctx, memberlist, "dances", data.dance)
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "danced with", "dance with", data.dance, "Dance")

    @bridge.bridge_command(brief="Blush")
    @option("members", str, description="Mention users that made you blush", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, *, members):
        """ Blush (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "blushes", data.blush)

    @bridge.bridge_command(brief="Be happy")
    @option("members", str, description="Mention users that made you happy", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx, *, members):
        """ Be happy (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "smiles", data.happy)

    @bridge.bridge_command(brief="Wag your tail ")
    @option("members", str, description="Mention users that made you wag", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wag(self, ctx, *, members):
        """ Wag your tail (Optionally because of specified people) """
        if not members:
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

    @bridge.bridge_command(brief="Give someone's avatar a rainbow overlay")
    @option("user", discord.Member, description="Select a user", required=False)
    @option("border", bool, description="Make it a border?", required=False, default=False)
    @option("server-avatar", bool, description="Use their server avatar?", required=False, default=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user=None, border=False, server_avatar=False):
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
