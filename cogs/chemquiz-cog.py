#!/usr/bin/python3
import discord
from discord.ext import commands
import random
from utils.orgachem import OrgaChem

class chemquiz(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
        self.keys = list(vars(OrgaChem()).keys())
        self.values = list(vars(OrgaChem()).values())


    @commands.command()
    async def chemquiz(self, ctx):
        await ctx.send(f'What\'s this functional group called?\n{self.values[(n := random.randint(0, len(self.values)))]}')
        reply = await self.Client.wait_for('message', check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel)
        if reply.content.lower() == (a := self.keys[n].lower()):
            await ctx.message.channel.send(f'Yep! Answer was \'{a}\'')
        else:
            await ctx.message.channel.send(f'Noooooooo.. Answer was \'{a}\'')

def setup(Client):
    Client.add_cog(chemquiz(Client))
