#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import os
import apis

class adventurecat(commands.Cog):

    def __init__(self, Client):
        self.Client = Client
        self.reddit = apis.apis().reddit
        self.limit = 50 # hot limit

    # Improvements necessary :
    # - Filter image posts
    # - Handle image galleries

    @commands.command()
    async def adventurecat(self, ctx):

        posts = [[post.title, post.author, post.url, post.permalink] for post in reddit.subreddit("adventurecats").hot(limit = self.limit)]

        images = list(filter(lambda p: 'i.redd.it' in p[2], posts[:1]))

        # galleries = list(filter(lambda p: 'gallery' in p[2], posts))
        #
        # if galleries:
        #     s = requests.Session()
        #     s.headers.update({'User-Agent': 'Thorlin-Bot'})
        #     imglinks = [re.search(r'https:\/\/preview.redd.it\/[a-z0-9]{13}\.jpg', s.get(galleries[i][2]).text).group() for i in range(len(galleries))]
        #     images += imglinks

        await ctx.send(random.choice(images[2]))

def setup(Client):
    Client.add_cog(adventurecat(Client))
