#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import os
import apis

class meowIRL(commands.Cog):
    def __init__(self, Client):
        self.Client = Client
        self.reddit = apis.apis().reddit
        self.limit = 50 # hot limit

    @commands.command()
    async def meowIRL(self, ctx):
        posts = [[post.author, post.url] for post in reddit.subreddit("MEOW_IRL").hot(limit = self.limit)]
        posts = list(filter(lambda p: '.gif' in p[2], posts[1:])) # rem pinned and gifs

        chosen = random.choice(posts)

        embed = discord.Embed(title = "MEOW!")
        embed.set_author(name = f'u/{chosen[0]}', url = f'https://reddit.com/u/{chosen[0]}')
        embed.set_image(url = chosen[1])

        await ctx.send(embed = embed)

def setup(Client):
    Client.add_cog(meowIRL(Client))









































# luca was here x)
