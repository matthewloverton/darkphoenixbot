import discord, datetime
from discord.ext import commands

class ServerCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['serverinfo', 'guildinfo', 'server'])
    async def server_info(self, ctx):
        now = datetime.datetime.now()
        creation = ctx.guild.created_at
        difference = now - creation
        embed = discord.Embed(title=f'**{ctx.guild.name}**', colour=discord.Colour(0x9013fe), description=f'Since {creation.strftime("%d %B %Y %H:%M")}. That\'s over {difference.days} days ago since the creation of {ctx.guild.name}!', timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.set_footer(text=f'Server ID: {ctx.guild.id}', icon_url=f'{ctx.author.avatar_url}')
        embed.add_field(name='Region', value=f'{ctx.guild.region}')
        embed.add_field(name='Users', value=f'{ctx.guild.member_count}/{ctx.guild.max_members}')
        embed.add_field(name='Text Channels', value=f'{len(ctx.guild.text_channels)}')
        embed.add_field(name='Voice Channels', value=f'{len(ctx.guild.voice_channels)}')
        embed.add_field(name='Roles', value=f'{len(ctx.guild.roles)}')
        embed.add_field(name='Owner', value=f'{ctx.guild.owner}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['userinfo', 'profile', 'user', 'memberinfo', 'member'])
    async def user_info(self, ctx, *, member: discord.Member = None):
        now = datetime.datetime.now()
        user = member if member else ctx.author
        title = f'**{user} - {user.nick}**' if user.nick else f'**{user}**'
        colour = user.colour
        description = f'status: {user.status}'
        creation = user.created_at
        joined = user.joined_at
        c_diff = now - creation
        j_diff = now - joined
        embed = discord.Embed(title=title, colour=colour, description=description, timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=f'{user.avatar_url}')
        embed.set_footer(text=f'User ID: {user.id}', icon_url=f'{ctx.author.avatar_url}')
        embed.add_field(name='Joined Discord on:', value=f'{creation.strftime("%d %B %Y %H:%M")}\n({c_diff.days} days ago)')
        embed.add_field(name='Joined this server on:', value=f'{joined.strftime("%d %B %Y %H:%M")}\n({j_diff.days} days ago)')
        if user.premium_since:
            nitro = user.premium_since
            n_diff = now - nitro
            embed.add_field(name='Nitro boosted server on:', value=f'{nitro.strftime("%d %B %Y &H:%M")}\n({n_diff.days}) days ago')
        embed.add_field(name='Roles:', value=f'{", ".join(str(role) for role in user.roles[1:])}')
        await ctx.send(embed=embed)

    @user_info.error
    async def user_info_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that member, please try again.")

#SETUP function to add this cog to the client when loaded.
def setup(client):
    client.add_cog(ServerCog(client))
