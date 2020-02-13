import discord, traceback, sys
from discord.ext import commands


class OwnerCog(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Hidden means it won't show up on the default help.
    # Loads a Module (use cogs.cogname).
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Unloads a Module.
    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    # Unloads a Module and the Loads it again.
    # Useful for developing to test if code is working without restarting the bot!
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cogs(self, ctx, *, cog: str):
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

def setup(client):
    client.add_cog(OwnerCog(client))
