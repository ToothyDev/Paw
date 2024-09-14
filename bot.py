import discord
from discord import Intents, Status, Activity, ActivityType

from config import token
import logger

log = logger.get_logger(__name__)

bot = discord.Bot(intents=discord.Intents.all(), status=Status.online,
                  activity=Activity(type=ActivityType.watching, name="over the Paw Kingdom"))

bot.load_extensions("cogs")
bot.load_extensions("cogs.events")
log.info("Loaded cogs: " + ', '.join(key for key in bot.cogs))


@bot.listen()
async def on_connect():
    log.info('Connected to Discord!')


@bot.listen()
async def on_ready():
    log.info(f'Logged in as {bot.user}')


bot.run(token)
