import discord
import random
from discord.ext import commands
import json

config = json.load(open('../config.json', 'r'))
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('PHOENIX BOT STARTED..')

@client.event
async def on_member_join(member):
    print(member.joined_at)

@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        async with channel.typing():
            await message.channel.send('Hello!')
            print('HELLO SENT.')

    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is doubtful.',
                 'No way.',
                 'Absolutely.',
                 'Definitely Not.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

client.run(config['discord']['token'])