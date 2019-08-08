import discord
import random
from discord.ext import commands
import json

config = json.load(open('config.json', 'r'))
client = commands.Bot(command_prefix = '/')

image_channels = ['resource-channel']
image_types = ['png', 'gif', 'jpg', 'jpeg', 'svg']

@client.event
async def on_ready():
    print('MINION OF AKU STARTED..')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.channel.name in image_channels:

        if not message.attachments and not message.content.startswith('http'):
            await message.author.send('#{0.channel.name} accepts only images. Please send an image!'.format(message))
            await message.delete()
        else:
            try:
                for attachment in message.attachments:
                    if attachment.filename.split('.')[-1] not in image_types:
                        await message.author.send('#{0.channel.name} accepts only images. Please send an image!'.format(message))
                        await message.delete()
            except:
                print('Unknown error')
    
    await client.process_commands(message)

@client.command()
async def snap(ctx, *, member: discord.Member):
    mentionid = client.get_user(159985870458322944)
    for role in ctx.author.roles:
        if role.name in ['Administrator', 'The Seven', 'Alliance Leader']:
            await member.kick()
            await ctx.send('{0} has been dusted by.. {1}'.format(member, mentionid.mention))

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def joined(ctx, *, member: discord.Member):
    for role in ctx.author.roles:
        if role.name in ['Administrator', 'The Seven', 'Alliance Leader']:
            await ctx.author.send('{0} joined on {0.joined_at}'.format(member))

client.run(config['discord']['token'])
