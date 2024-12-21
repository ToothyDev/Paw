import random
import time

import discord
from discord import slash_command, option
from discord.ext import commands

import assets
import utils
from utils import build_input_history


class Socials(discord.Cog, name="Socials"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.last_revived = 0
        self.ai_enabled = utils.is_ai_enabled()

    @slash_command()
    @option("topic", str, description="The topic to revive chat with", required=False)
    async def chat_revival(self, ctx: discord.ApplicationContext, topic: str):
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
    async def snuggle(self, ctx: discord.ApplicationContext, members: str):
        words = ["snuggled", "Snuggle"]
        await utils.social_interaction_handler(ctx, members, words, assets.SNUGGLE)

    @slash_command()
    @option("members", str, description="Mention users to hug")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx: discord.ApplicationContext, members: str):
        """ Hug the specified people """
        words = ["hugged", "Hug"]
        await utils.social_interaction_handler(ctx, members, words, assets.HUG)

    @slash_command()
    @option("members", str, description="Mention users to boop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx: discord.ApplicationContext, members: str):
        words = ["booped", "Boop"]
        await utils.social_interaction_handler(ctx, members, words, assets.BOOP)

    @slash_command()
    @option("members", str, description="Mention users to kiss")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx: discord.ApplicationContext, members: str):
        """ Kiss the specified people """
        words = ["kissed", "Kiss"]
        await utils.social_interaction_handler(ctx, members, words, assets.KISS)

    @slash_command()
    @option("members", str, description="Mention users to lick")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx: discord.ApplicationContext, members: str):
        """ Lick the specified people """
        words = ["licked", "Lick"]
        await utils.social_interaction_handler(ctx, members, words, assets.LICK)

    @slash_command()
    @option("members", str, description="Mention users to bellrub")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx: discord.ApplicationContext, members: str):
        """ Give bellyrubs to the specified people """
        words = ["rubbed the belly of", "Rub", "given bellyrubs"]
        await utils.social_interaction_handler(ctx, members, words, assets.BELLYRUB)

    @slash_command()
    @option("members", str, description="Mention users to nuzzle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx: discord.ApplicationContext, members: str):
        """ Nuzzle the specified people """
        words = ["nuzzled", "Nuzzle"]
        await utils.social_interaction_handler(ctx, members, words, assets.NUZZLE)

    @slash_command()
    @option("members", str, description="Mention users to cuddle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx: discord.ApplicationContext, members: str):
        """ Cuddle the specified people """
        words = ["cuddled", "Cuddle"]
        await utils.social_interaction_handler(ctx, members, words, assets.CUDDLE)

    @slash_command()
    @option("members", str, description="Mention users to feed")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx: discord.ApplicationContext, members: str):
        """ Feed the specified people """
        words = ["fed", "Feed"]
        await utils.social_interaction_handler(ctx, members, words, assets.FEED)

    @slash_command()
    @option("members", str, description="Mention users to glomp")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx: discord.ApplicationContext, members: str):
        """ Glomp on the specified people """
        words = ["glomped", "Glomp"]
        await utils.social_interaction_handler(ctx, members, words, assets.GLOMP)

    @slash_command()
    @option("members", str, description="Mention users to highfive")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx: discord.ApplicationContext, members: str):
        """ Highfive the specified people """
        words = ["highfived", "Highfive"]
        await utils.social_interaction_handler(ctx, members, words, assets.HIGHFIVE)

    @slash_command()
    @option("members", str, description="Mention users to rawr at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx: discord.ApplicationContext, members: str):
        """ Rawr at the specified people """
        words = ["rawred at", "Rawr"]
        await utils.social_interaction_handler(ctx, members, words, assets.RAWR)

    @slash_command()
    @option("members", str, description="Mention users to howl at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def howl(self, ctx: discord.ApplicationContext, members: str):
        """ Howl at the specified people """
        words = ["howled at", "Howl"]
        await utils.social_interaction_handler(ctx, members, words, assets.HOWL)

    @slash_command()
    @option("members", str, description="Mention users to pat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx: discord.ApplicationContext, members: str):
        """ Pat the specified people """
        words = ["pats", "Pat", "Pat"]
        await utils.social_interaction_handler(ctx, members, words, assets.PET)

    @slash_command()
    @option("members", str, description="Mention users to give a cookie to")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx: discord.ApplicationContext, members: str):
        """ Give cookies to the specified people """
        words = ["gave a cookie to", "Give a cookie", "given a cookie"]
        await utils.social_interaction_handler(ctx, members, words, assets.COOKIE)

    @slash_command()
    @option("members", str, description="Mention users to dance with", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dance(self, ctx: discord.ApplicationContext, members: str):
        """ Dance with someone """
        if not members:
            memberlist = None
            return await utils.feelings(ctx, memberlist, "dances", assets.DANCE)
        words = ["danced with", "Dance"]
        await utils.social_interaction_handler(ctx, members, words, assets.DANCE)

    @slash_command()
    @option("members", str, description="Mention users that made you blush", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx: discord.ApplicationContext, members: str):
        """ Blush (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await utils.mention_converter(ctx, members)
            if not memberlist:
                return
        await utils.feelings(ctx, memberlist, "blushes", assets.BLUSH)

    @slash_command()
    @option("members", str, description="Mention users that made you happy", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx: discord.ApplicationContext, members: str):
        """ Be happy (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await utils.mention_converter(ctx, members)
            if not memberlist:
                return
        await utils.feelings(ctx, memberlist, "smiles", assets.HAPPY)

    @slash_command()
    @option("members", str, description="Mention users that made you wag", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wag(self, ctx: discord.ApplicationContext, members: str):
        """ Wag your tail (Optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await utils.mention_converter(ctx, members)
            if not memberlist:
                return
        await utils.feelings(ctx, memberlist, "wags their tail", assets.WAG)

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx: discord.ApplicationContext):
        """ Get a random animal fact """
        json = await utils.apireq(random.choice(utils.FACT_URLS))
        await ctx.respond(json.get("fact"))

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx: discord.ApplicationContext):
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
    async def gay(self, ctx: discord.ApplicationContext, user=None, border=False, server_avatar=True):
        """ Gay overlay on avatar """
        if not user:
            user = ctx.author
        url = user.display_avatar.url if server_avatar else user.avatar.url
        link = f"https://some-random-api.com/canvas/misc/lgbt/?avatar={url}" if border else f"https://some-random-api.com/canvas/gay/?avatar={url}"
        embed = discord.Embed(color=discord.Color.random())
        embed.set_image(url=link)
        embed.set_footer(text=f"Gay avatar: {user.display_name}")
        await ctx.respond(embed=embed)

    @slash_command(contexts={discord.InteractionContextType.guild})
    @option("text", str, description="What do you want to tell Paw?")
    async def gpt(self, ctx: discord.ApplicationContext, text: str):
        """ Talk to Paw! """
        if not self.ai_enabled:
            return await ctx.respond("AI functions are disabled due to missing (or invalid) API key, please contact the bot owner to fix this.")
        await ctx.defer()
        input_history = await build_input_history(self.bot, ctx, text)
        response = await utils.generate_from_history(input_history)
        await ctx.respond(content=f"**Prompt:** {text}\n**Paw:** {response}")


def setup(bot: discord.Bot):
    bot.add_cog(Socials(bot))
