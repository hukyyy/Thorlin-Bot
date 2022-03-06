#!/usr/bin/python3
import discord
from discord.ext import commands
import random

class showerthought(commands.Cog):
    def __init__(self, Client, reddit):
        self.Client = Client
        self.reddit = reddit
        self.limit = 50 # hot limit
        self.color = 0xd4f1f9

    @commands.Command()
    async def showerthought(self, ctx):

        thoughts = [[thought.title, thought.author, thought.permalink] for thought in reddit.subreddit("showerthoughts").hot(limit = self.limit)]

        chosen = random.choice(thoughts)

        embed = discord.Embed(
            title = chosen[0],
            description = f'[Thought]({chosen[2]}) by [u/{chosen[1]}](https://reddit.com/u/{chosen[1]}) on [r/showerthoughts](https://reddit.com/r/showerthoughts)',
            color = self.color
        )

        await ctx.send(embed = embed)

def setup(Client, reddit):
    Client.add_cog(showerthought(Client, reddit))
