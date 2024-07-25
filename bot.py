import discord
from discord import Intents, Status, Activity, ActivityType

from config import token

intents = Intents(guilds=True, guild_messages=True, message_content=True, members=True)

bot = discord.Bot(intents=intents, status=Status.dnd, activity=Activity(type=ActivityType.watching, name="you"))

bot.load_extensions("cogs")
bot.load_extensions("cogs.events")
print(bot.extensions)


@bot.listen()
async def on_connect():
    print('Connected to Discord!')


@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')


bot.run(token)
