#!/usr/bin/python3
import discord
from discord.ext import commands
import random

class adventurecat(commands.Cog):

    def __init__(self, Client, reddit):
        self.Client = Client
        self.reddit = reddit

    # Improvements necessary :
    # - Filter image posts
    # - Handle image galleries

    @commands.Command()
    async def adventurecat(self, ctx):

        posts = [[post.title, post.author, post.url, post.permalink] for post in reddit.subreddit("adventurecats").hot(limit = 50)]

        images = list(filter(lambda p: 'i.redd.it' in p[2], posts))

        # galleries = list(filter(lambda p: 'gallery' in p[2], posts))
        #
        # if galleries:
        #     s = requests.Session()
        #     s.headers.update({'User-Agent': 'Thorlin-Bot'})
        #     imglinks = [re.search(r'https:\/\/preview.redd.it\/[a-z0-9]{13}\.jpg', s.get(galleries[i][2]).text).group() for i in range(len(galleries))]
        #     images += imglinks

        await ctx.send(random.choice(images[2]))

def setup(Client, reddit):
    Client.add_cog(adventurecat(Client, reddit))
