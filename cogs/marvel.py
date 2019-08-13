import discord
from discord.ext import commands
import os.path
from tinydb import TinyDB, Query
import re, datetime

abspath = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(abspath, '../db.json')
db = TinyDB(path)

class MarvelCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['stat', 'char', 'character', 'hero'])
    async def stats(self, ctx, *, hero: str):
        Character = Query()
        characters = db.table('Characters')
        search = characters.search((Character.Aliases.any(f'{hero.lower()}')) | (Character.Name.matches(f'{hero}', flags=re.IGNORECASE)))
        if search:
            for result in search:
                embed = discord.Embed(title=f'**{result["Name"]}**', colour=ctx.author.colour, description=f'*{" - ".join(str(tag) for tag in result["Tags"])}*', timestamp=datetime.datetime.now())
                embed.set_thumbnail(url=f'{result["Portrait_URL"]}')
                embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                embed.add_field(name='Speed:', value=f'{result["Speed"]}')
                embed.add_field(name='Health:', value=f'{result["Health"]}')
                embed.add_field(name='Damage:', value=f'{result["Damage"]}')
                embed.add_field(name='Focus:', value=f'{result["Focus"]}')
                embed.add_field(name='Accuracy:', value=f'{result["Accuracy"]}')
                embed.add_field(name='Crit Chance:', value=f'{result["Crit Chance"]}')
                embed.add_field(name='Crit Damage:', value=f'{result["Crit Damage"]}')
                embed.add_field(name='Armor:', value=f'{result["Armor"]}')
                embed.add_field(name='Resistance:', value=f'{result["Resistance"]}')
                embed.add_field(name='Dodge Chance:', value=f'{result["Dodge Chance"]}')
                embed.add_field(name='Block Chance:', value=f'{result["Block Chance"]}')
                await ctx.send(embed=embed)
        else:
            await ctx.send(f'Unable to find a character matching that name.')

    @commands.command(aliases=['moves'])
    async def abilities(self, ctx, *, hero: str = None):
        if not hero:
            embed = discord.Embed(title='**Abilities Help**', description='`/moves | /abilities <character(s)>`\nExamples:\n> /moves black panther\n> /abilities a.i.m', colour=ctx.author.colour, timestamp=datetime.datetime.now())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name='__Ability - Name - (Starting Energy/Energy Cost)__', value='Ability description is here')
            embed.add_field(name='__Status Effects and Tags__', value='**Bold** items are Status Effects\n`/effect | /status | /buff /debuff <status effect>`\nExample:\n> /effect Defense Up\n __Underlined__ items are Tags\n`/tags <tag1> <tag2> etc.`\nExample: \n> /tags Hero Brawler', inline=False)
            await ctx.send(embed=embed)
            return
        Character = Query()
        characters = db.table('Characters')
        search = characters.search((Character.Aliases.any(f'{hero.lower()}')) | (Character.Name.matches(f'{hero}', flags=re.IGNORECASE)))
        if search:
            for result in search:
                embed = discord.Embed(title=f'**{result["Name"]}**', colour=ctx.author.colour, description=f'*{" - ".join(str(tag) for tag in result["Tags"])}*', timestamp=datetime.datetime.now())
                embed.set_thumbnail(url=f'{result["Portrait_URL"]}')
                embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                embed.add_field(name=f'__Basic - {result["Abilities"]["Basic"]["Name"]}__ :', value=f'{result["Abilities"]["Basic"]["Description"]}')
                embed.add_field(name=f'__Special - {result["Abilities"]["Special"]["Name"]} - ({result["Abilities"]["Special"]["Starting Energy"]}/{result["Abilities"]["Special"]["Energy Cost"]})__ :', value=f'{result["Abilities"]["Special"]["Description"]}')
                if 'Minion' not in result["Tags"]:
                    embed.add_field(name=f'__Ultimate - {result["Abilities"]["Ultimate"]["Name"]} - ({result["Abilities"]["Ultimate"]["Starting Energy"]}/{result["Abilities"]["Ultimate"]["Energy Cost"]})__ :', value=f'{result["Abilities"]["Ultimate"]["Description"]}')
                embed.add_field(name=f'__Passive - {result["Abilities"]["Passive"]["Name"]}__ :', value=f'{result["Abilities"]["Passive"]["Description"]}')
                await ctx.send(embed=embed)
        else:
            await ctx.send('Unable to find a character matching that name.')

    @abilities.error
    async def abilities_handler(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"Abilities for that character have not been implemented yet.")
    
    @commands.command()
    async def tags(self, ctx, *args):
        Name = Query()
        tags = db.table('Tags')
        if not args:
            embed = discord.Embed(title='**Tags Help - Available Tags**', description='`/tags <tag1> <tag2> etc.`\nExamples:\n> /tags Hero Brawler\n> /tags Villain Mystic Controller', colour=ctx.author.colour, timestamp=datetime.datetime.now())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name='Side', value=f'{", ".join((tags.get(Name.Name == "Side")["Tags"]))}', inline=False)
            embed.add_field(name='Trait', value=f'{", ".join((tags.get(Name.Name == "Trait")["Tags"]))}', inline=False)
            embed.add_field(name='Origin', value=f'{", ".join((tags.get(Name.Name == "Origin")["Tags"]))}', inline=False)
            embed.add_field(name='Team', value=f'{", ".join((tags.get(Name.Name == "Team")["Tags"]))}', inline=False)
            embed.add_field(name='Role', value=f'{", ".join((tags.get(Name.Name == "Role")["Tags"]))}', inline=False)
            embed.add_field(name='Other', value=f'{", ".join((tags.get(Name.Name == "Other")["Tags"]))}',inline=False)
            await ctx.send(embed=embed)
        else:
            Character = Query()
            characters = db.table('Characters')
            search = characters.search(Character.Tags.all(args))
            if search:
                embed = discord.Embed(title=f'**{" - ".join(str(tag) for tag in args)}**', colour=ctx.author.colour, description=f'{", ".join(str(hero["Name"]) for hero in search)}', timestamp=datetime.datetime.now())
                embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                await ctx.send(embed=embed)
            else:
                await ctx.send('Unable to find any characters matching those tags.')

    @commands.command(aliases=['status', 'effect', 'buff', 'debuff'])
    async def status_effect(self, ctx, *, effect: str = None):
        Effect = Query()
        effects = db.table('Effects')
        if not effect:
            embed = discord.Embed(title='**Status Effect Help - Available Status Effects**', description='`/status | /effect | /buff | /debuff <status effect>`\nExamples:\n> /status Heal Block\n> /buff Defense Up', colour=ctx.author.colour, timestamp=datetime.datetime.now())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name='Positive', value=f'{", ".join(str(effect["Name"]) for effect in (effects.search(Effect.Category == "Positive")))}', inline=False)
            embed.add_field(name='Negative', value=f'{", ".join(str(effect["Name"]) for effect in (effects.search(Effect.Category == "Negative")))}', inline=False)
            await ctx.send(embed=embed)
        else:
            search = effects.search(Effect.Name.matches(effect, flags=re.IGNORECASE))
            if search:
                print(search)
                embed = discord.Embed(title=f'{search[0]["Name"]}', description=f'{search[0]["Description"]}',colour=ctx.author.colour, timestamp=datetime.datetime.now())
                embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                await ctx.send(embed=embed)
            else:
                await ctx.send('Unable to find any effects that match.')

def setup(client):
    client.add_cog(MarvelCog(client))
