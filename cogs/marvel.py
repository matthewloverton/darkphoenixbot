import discord
from discord.ext import commands
import os.path
from tinydb import TinyDB, Query
import re, datetime

abspath = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(abspath, '../db.json')
db = TinyDB(path)

tags = {'Side': ['Hero', 'Villain'],
        'Trait': ['Bio', 'Mutant', 'Mystic', 'Skill', 'Tech'],
        'Origin': ['Asgard', 'City', 'Cosmic', 'Global'],
        'Team': ['Aim', 'Avenger', 'Brotherhood', 'Defender', 'FantasticFour', 'Guardian', 'Hand', 'Hydra', 'Kree',
                 'Mercenary', 'Ravager', 'Shield', 'SinisterSix', 'SpiderVerse', 'Wave1Avenger', 'Xmen', 'Xforce'],
        'Role': ['Blaster', 'Brawler','Controller', 'Protector', 'Support'],
        'Other': ['Eternal','Inhuman', 'MartialArtist', 'Minion', 'Mutant', 'Marvel80th', 'Military', 'PowerArmor']
        }

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
    async def abilities(self, ctx, *, hero: str):
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
        if not args:
            embed = discord.Embed(title='**Available Tags**', colour=ctx.author.colour, timestamp=datetime.datetime.now())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name='Side', value=f'{", ".join(tags["Side"])}')
            embed.add_field(name='Trait', value=f'{", ".join(tags["Trait"])}')
            embed.add_field(name='Origin', value=f'{", ".join(tags["Origin"])}')
            embed.add_field(name='Team', value=f'{", ".join(tags["Team"])}')
            embed.add_field(name='Role', value=f'{", ".join(tags["Role"])}')
            embed.add_field(name='Other', value=f'{", ".join(tags["Other"])}')
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

def setup(client):
    client.add_cog(MarvelCog(client))
