from discord.ext import commands
from secrets import owner

bg_bot = commands.Bot(command_prefix='!')

@bg_bot.event  # do all this stuff when bot connects successfully
async def on_ready():
    bot.owner_id = secrets.owner
    print(f'Logged in as {bot.user.name}!')
