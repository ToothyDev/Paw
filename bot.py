from discord import Intents, Status, Activity, ActivityType
from discord.ext import commands, bridge
import discord
from config import token

intents = Intents(guilds=True, guild_messages=True, message_content=True, members=True)
# intents.message_content = True #Uncomment this if you use prefixed command that are not mentions
bot = bridge.Bot(intents=intents, command_prefix=">>", status=Status.dnd,
                 activity=Activity(type=ActivityType.watching, name="you (prefix: >>)"))


class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)


bot.help_command = MyNewHelp()

bot.load_extension('jishaku')
bot.load_extensions("cogs")  # Loads all cogs in the cogs folder
bot.load_extensions("cogs.events")
print(bot.extensions)
BOOTED = False


@bot.listen()
async def on_connect():
    print('Connected to Discord!')


@bot.listen()
async def on_ready():
    global BOOTED
    if BOOTED:
        print("Reconnect(?)")
    if not BOOTED:
        # await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
        print(f'Logged in as {bot.user}')
        print('------')
        BOOTED = True


bot.run(token)
