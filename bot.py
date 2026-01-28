import discord
from discord import Status, Activity, ActivityType

from config import token
import logger

log = logger.get_logger(__name__)

bot = discord.Bot(intents=discord.Intents.all(), status=Status.online,
                  activity=Activity(type=ActivityType.custom, name="Watching over the Paw Kingdom"))

bot.load_extensions("cogs")
bot.load_extensions("cogs.events")
log.info("Loaded cogs: " + ', '.join(list(bot.cogs)))


@bot.listen()
async def on_connect():
    log.info('Connected to Discord!')


@bot.listen()
async def on_ready():
    log.info(f'Logged in as {bot.user}')


bot.run(token)
