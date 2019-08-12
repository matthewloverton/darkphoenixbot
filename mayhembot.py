import discord
from discord.ext import commands
import json, sys, traceback, asyncio, random
#from tinydb import TinyDB, Query

config = json.load(open('config.json', 'r'))
#db = TinyDB('db.json')

#Define channels to auto-delete messages that do not contain the image_types.
image_channels = ['resource-channel']
image_types = ['png', 'gif', 'jpg', 'jpeg', 'svg']

#0 = Playing
#1 = Streaming
#2 = Listening to
#3 = Watching

#Define bot statuses
statuses = [['with the Empire', 0],
            ['over the Empire', 3],
            ['some lo-fi beats', 2],
            ['with Aku\'s son', 0],
            ['alliances go to war', 3],
            ['complaints about MSF', 2],
            ['ZIO4 annoying Aku with his ideas', 2],
            ['Blade bragging about his Rocket', 2]]

#INITIALIZE BOT CLIENT
def get_prefix(bot, message):
    prefixes = ['/']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.members',
                      'cogs.moderation',
                      'cogs.server',
                      'cogs.marvel',
                      'cogs.owner']

client = commands.Bot(command_prefix = get_prefix, description = "Minion of Aku, the Mayhem empire's very own server manager.")

#FUNCTIONS

async def status_task():
    while True:
        status = random.choice(statuses)
        await client.change_presence(activity=discord.Activity(name=status[0], type=status[1]))
        await asyncio.sleep(180)


#LOAD COGS
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

# Print information about the bot if it successfully activates.
@client.event
async def on_ready():
    print (f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')

    # Change the bot status
    client.loop.create_task(status_task())
    print(f'Successfully logged in and running...!')

#@client.command()
#async def stats(ctx, *, hero: str):
#    Character = Query()
#    characters = db.table('Characters')
#    print(characters)
#    await ctx.send('STATS')

client.run(config['discord']['token'], bot = True, reconnect = True)
