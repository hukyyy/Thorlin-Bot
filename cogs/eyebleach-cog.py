#!/usr/bin/python3
import discord
from discord.ext import commands

import random

class eyebleach(commands.Cog):
    def __init__(self, Client, reddit):
        self.Client = Client
        self.reddit = reddit
        self.limit = 50 # hot limit

    @commands.Command()
    async def eyebleach(self, ctx):
        posts = [[post.title, post.author, post.url] for post in reddit.subreddit("Eyebleach").hot(limit = self.limit)]

        posts = list(filter(lambda p: '.gif' in p[2], posts[1:])) # rem pinned and gifs
        # posts.remove(posts[0]) # rem pinned post

        chosen = random.choice(posts)

        embed = discord.Embed(title = chosen[0])
        embed.set_author(name = f"u/{chosen[1]}", url = f'https://reddit.com/u/{chosen[1]}')
        embed.set_image(url = chosen[2])

        await ctx.send(embed = embed)

def init(Client, reddit):
    Client.add_cog(eyebleach(Client, reddit))
