import discord, datetime
from discord.ext import commands

class MembersCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #ADMIN COMMANDS

    # Sends a message to the author when the member joined.
    @commands.command()
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def joined(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send('Please specify a member to be checked.')
        date = member.joined_at.strftime("%A %d %B %Y at %H:%M")
        await ctx.author.send(f'{member.display_name} joined on {date}')

    # Kicks a member from the server, tags F.R.I.D.A.Y.
    @commands.command()
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def snap(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send('Please specifiy a member to be kicked.')
            return
        mentionid = self.client.get_user(159985870458322944)
        await member.kick()
        if mentionid:
            await ctx.send(f'{member.name} has been dusted by.. {mentionid.mention}')
        else:
            await ctx.send(f'{member.name} has been dusted..')

    # Renames a member from the server.
    @commands.command()
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def rename(self, ctx, member: discord.Member = None, nick: str = None):
        if not member:
            await ctx.send('Please specify a member to be renamed.')
            return
        oldname = member.display_name
        await member.edit(nick = nick)
        if not nick:
            await ctx.send(f'{member.mention}\'s nickname has been removed.')
        else:
            await ctx.send(f'{oldname}\'s nickname has been changed to {member.mention}')

    # Mutes a member in the server.
    @commands.command(aliases=['silence'])
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def mute(self, ctx, member: discord.Member = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not member:
            await ctx.send('Please specify a member to be muted.')
            return
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been muted.')

    # Unmutes a member in the server.
    @commands.command()
    @commands.has_any_role('Administrator', 'The Seven', 'Alliance Leader')
    async def unmute(self, ctx, member: discord.Member = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not member:
            await ctx.send('Please specify a member to be unmuted.')
            return
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has been unmuted.')

    @commands.command(aliases=['serverinfo', 'guildinfo'])
    async def server_info(self, ctx):
        now = datetime.datetime.now()
        creation = ctx.guild.created_at
        difference = now - creation
        embed = discord.Embed(title=f'**{ctx.guild.name}**', colour=discord.Colour(0x9013fe), description=f'Since {creation.strftime("%d %B %Y %H:%M")}. That\'s over {difference.days} days ago since the creation of {ctx.guild.name}!', timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.set_footer(text=f'Server ID: {ctx.guild.id}', icon_url=f'{ctx.author.avatar_url}')
        embed.add_field(name='Region', value=f'{ctx.guild.region}')
        embed.add_field(name='Users', value=f'{ctx.guild.member_count}')
        embed.add_field(name='Text Channels', value=f'{len(ctx.guild.text_channels)}')
        embed.add_field(name='Voice Channels', value=f'{len(ctx.guild.voice_channels)}')
        embed.add_field(name='Roles', value=f'{len(ctx.guild.roles)}')
        embed.add_field(name='Owner', value=f'{ctx.guild.owner}')
        await ctx.send(embed=embed)

#SETUP function to add this cog to the client when loaded.
def setup(client):
    client.add_cog(MembersCog(client))
