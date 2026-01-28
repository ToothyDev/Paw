import discord

import logger
from config import token

log = logger.get_logger(__name__)

bot = discord.Bot(intents=discord.Intents.all(), status=discord.Status.online,
                  activity=discord.Activity(type=discord.ActivityType.custom, state="Watching over The Paw Kingdom"))

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
