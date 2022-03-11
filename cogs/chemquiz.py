#!/usr/bin/python3
import discord
from discord.ext import commands
import random
from utils.orgachem import OrgaChem

class chemquiz(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
        self.OrgaChem = OrgaChem()

    @commands.command()
    async def chemquiz(self, ctx):
        pick = random.choice(self.OrgaChem.compounds)

        await ctx.send(f'What\'s this functional group called? \n {pick[-1]}')

        reply = await self.Client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

        answers = pick[0:-1] # -> [english, french*, structure]

        if reply.content.lower() in answers:
            await ctx.send(f'Yep! Answer was \'{answers[0]}\' (\'{answers[1]}\')')
        else:
            await ctx.send(f'Noooooooo.. Answer was \'{answers[0]}\' (\'{answers[1]}\')')

def setup(Client):
    Client.add_cog(chemquiz(Client))
