import discord, datetime
from discord.ext import commands

#Define channels to auto-delete messages that do not contain the image_types.
image_channels = ['resource-channel']
image_types = ['png', 'gif', 'jpg', 'jpeg', 'svg']

class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client    

    @commands.Cog.listener() 
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        if message.channel.name in image_channels:
            if not message.attachments and not message.content.startswith('http'):
                await message.author.send(f'#{message.channel.name} accepts only images. Please send an image!')
                await message.delete()
            else:
                for attachment in message.attachments:
                    if attachment.filename.split('.')[-1] not in image_types:
                        await message.author.send(f'#{message.channel.name} accepts only images. Please send an image!')
                        await message.delete()

#SETUP function to add this cog to the client when loaded.
def setup(client):
    client.add_cog(ModerationCog(client))
