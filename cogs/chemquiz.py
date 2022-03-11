#!/usr/bin/python3
import discord
from discord.ext import commands
import random
from utils.orgachem import OrgaChem

class chemquiz(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
        self.OrgaChem = OrgaChem()

    def check(self, m) -> bool:
        return m.author == ctx.author and m.channel == ctx.channel


    @commands.command()
    async def chemquiz(self, ctx):
        pick = random.choice(self.OrgaChem.compounds)

        await ctx.send(f'What\'s this functional group called? \n {pick[-1]}')

        reply = await self.Client.wait_for('message', check=self.check())

        answers = pick[0:-2] # -> [english, french*, structure]

        if reply.content.lower() in answers:
            ctx.send(f'Yep! Answer was \'{answers[0]}\' (\'{answers[1]}\')')
        else:
            ctx.send(f'Noooooooo.. Answer was \'{answers[0]}\' (\'{answers[1]}\')')

def setup(Client):
    Client.add_cog(chemquiz(Client))
