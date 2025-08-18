import io
import random
import time

import aiohttp
import discord
import openai
from discord import slash_command, option
from discord.ext import commands

import logger
import utils
from utils import build_input_history
from views.pet_interactions_view import PetInteractionView

log = logger.get_logger(__name__)


class Socials(discord.Cog, name="Socials"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.last_revived = 0

        for command in utils.data.SOCIAL_COMMANDS_DATA:
            self._create_social_command(command["name"], command["description"], command["option_description"],
                                        command["words"], command["gifs"])

        for command in utils.data.EMOTION_COMMANDS_DATA:
            self._create_emotion_command(command["name"], command["description"], command["option_description"],
                                         command["word"], command["gifs"])

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content.startswith(self.bot.user.mention) and message.guild:
            async with message.channel.typing():
                input_history = await build_input_history(self.bot, message.channel, message.author, message.guild,
                                                          message.clean_content)
                try:
                    response = await utils.generate_from_history(input_history)
                    await message.reply(response)
                except openai.APIError as e:
                    await message.reply("An unknown error occured! This will be logged and fixed!")
                    log.error(
                        f"{message.author.global_name} used @Paw which caused '{e}', error class: {e.__class__.__name__}",
                        exc_info=(type(e), e, e.__traceback__))

    @slash_command()
    @option("topic", str, description="The topic to revive chat with", required=False)
    async def chat_revival(self, ctx, topic):
        """ Revive the chat! """
        revival_role = ctx.guild.get_role(738356235841175594)
        if revival_role not in ctx.author.roles:
            await ctx.respond("You need the chat revival role to revive the chat! Get it in <id:customize>",
                              ephemeral=True)
            return
        if time.time() - 7200 <= self.last_revived:
            await ctx.respond("Chat was revived less than 2 hours ago!", ephemeral=True)
            return
        self.last_revived = time.time()
        await ctx.respond(
            f"<@&738356235841175594>! {topic if topic else 'Talk about something interesting!'}",
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=[revival_role]))

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        """ Get a random animal fact """
        json = await utils.apireq(random.choice(utils.FACT_URLS))
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
        if border:
            link = f"https://some-random-api.com/canvas/misc/lgbt/?avatar={url}"
        else:
            link = f"https://some-random-api.com/canvas/gay/?avatar={url}"
        embed = discord.Embed(color=discord.Color.random())
        embed.set_image(url=link)
        embed.set_footer(text=f"Gay avatar: {user.display_name}")
        await ctx.respond(embed=embed)

    @slash_command(contexts={discord.InteractionContextType.guild})
    @option("text", str, description="What do you want to tell Paw?")
    async def gpt(self, ctx: discord.ApplicationContext, text: str):
        """ Talk to Paw! """
        await ctx.defer()
        input_history = await build_input_history(self.bot, ctx.channel, ctx.author, ctx.guild, text)
        response = await utils.generate_from_history(input_history)
        await ctx.respond(content=f"**Prompt:** {text}\n**Paw:** {response}")

    @slash_command()
    @option("member", discord.Member, description="Select a member to pet")
    async def petpet(self, ctx: discord.ApplicationContext, member: discord.Member):
        """ Pet a user's avatar! """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.some-random-api.com/premium/petpet?avatar={member.display_avatar.with_format('png').with_size(256).url}") as resp:
                gif_file = discord.File(io.BytesIO(await resp.read()), filename="petpet.gif")

        components = [
            discord.ui.Container(
                discord.ui.TextDisplay(f"**{ctx.author.mention}** pet **{member.mention}**!"),
                discord.ui.MediaGallery(
                    discord.MediaGalleryItem(
                        url="attachment://petpet.gif")
                ),
                color=discord.Color.blue()
            )
        ]
        await ctx.respond(view=PetInteractionView(ctx, member, gif_file, *components), file=gif_file,
                          allowed_mentions=discord.AllowedMentions(users=[member]))

    def _create_social_command(self, name: str, description: str, option_description: str, words: list[str],
                               gifs: list[str]):
        @slash_command(name=name, description=description)
        @option("members", str, description=option_description)
        async def command_function(_cog: Socials, ctx: discord.ApplicationContext, members: str):
            await utils.social_interaction_handler(ctx, members, words, gifs)

        command_function.cog = self
        self.bot.add_application_command(command_function)  # type: ignore

    def _create_emotion_command(self, name: str, description: str, option_description: str, word: str, gifs: list[str]):
        @slash_command(name=name, description=description)
        @option("members", str, description=option_description, required=False)
        async def command_function(_cog: Socials, ctx: discord.ApplicationContext, members: str):
            if not members:
                memberlist = None
            else:
                memberlist = await utils.mention_converter(ctx, members)
                if not memberlist:
                    return
            await utils.feelings(ctx, memberlist, word, gifs)

        command_function.cog = self
        self.bot.add_application_command(command_function)  # type: ignore


def setup(bot):
    bot.add_cog(Socials(bot))
