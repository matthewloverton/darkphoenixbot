import discord
import random
from discord.ext import commands
import json, sys, traceback

config = json.load(open('config.json', 'r'))

#Define channels to auto-delete messages that do not contain the image_types.
image_channels = ['resource-channel']
image_types = ['png', 'gif', 'jpg', 'jpeg', 'svg']

#FUNCTIONS
def get_prefix(bot, message):
    prefixes = ['/']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.members',
                      'cogs.moderation',
                      'cogs.owner']

#INITIALIZE BOT CLIENT
client = commands.Bot(command_prefix = get_prefix, description = "Minion of Aku, the Mayhem empire's very own server manager.")

#LOAD COGS
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

# Print information about the bot if it successfully activates.
@client.event
async def on_ready():
    print (f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')

    # Change the bot status
    await client.change_presence(activity=discord.Game(name='with the Mayhem Server'))
    print(f'Successfully logged in and running...!')

client.run(config['discord']['token'], bot = True, reconnect = True)
