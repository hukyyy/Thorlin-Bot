#!/usr/bin/python3
import discord
from discord.ext import commands

class special(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
        self.surfers = 0

    async def add_surfer(self) -> int:
        self.surfers += 1
        return self.surfers

    @commands.command()
    async def surfer(self, ctx):
        await self.add_surfer()
        await ctx.send(f'{self.surfers} surfers!')


def setup(Client):
    Client.add_cog(special(Client))
