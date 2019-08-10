import discord, datetime
from discord.ext import commands


class MembersCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #ADMIN COMMANDS

    # Sends a message to the author when the member joined.
    @commands.command()
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def joined(self, ctx, *, member: discord.Member):
        date = member.joined_at.strftime("%A %d %B %Y at %H:%M")
        await ctx.author.send(f'{member.display_name} joined on {date}')

    # Kicks a member from the server, tags F.R.I.D.A.Y
    @commands.command()
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def snap(self, ctx, *, member: discord.Member):
        mentionid = client.get_user(159985870458322944)
        await member.kick()
        await ctx.send(f'{member.name} has been dusted by.. {mentionid.mention}')

#SETUP function to add this cog to the client when loaded.
def setup(client):
    client.add_cog(MembersCog(client))
