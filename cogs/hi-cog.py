import discord
from discord.ext import commands

class hi(commands.Cog):

    def __init__(self, Client):
        self.Client = Client

    @commands.Command()
    async def hi(self, ctx):
        await ctx.send(f"Hello, {ctx.message.author.name}!")

def setup(Client):
    Client.add_cog(hi(Client))
