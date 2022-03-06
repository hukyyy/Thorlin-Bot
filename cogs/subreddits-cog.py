#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import os
import apis

class subreddits(commands.Cog):

    def __init__(self, Client):
        self.Client = Client
        self.reddit = apis.apis().reddit
        self.limit = 50 # hot limit
        self.showercolor = 0xd4f1f9

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


    @commands.command()
    async def eyebleach(self, ctx):
        posts = [[post.title, post.author, post.url] for post in reddit.subreddit("Eyebleach").hot(limit = self.limit)]

        posts = list(filter(lambda p: '.gif' in p[2], posts[1:])) # rem pinned and gifs
        # posts.remove(posts[0]) # rem pinned post

        chosen = random.choice(posts)

        embed = discord.Embed(title = chosen[0])
        embed.set_author(name = f"u/{chosen[1]}", url = f'https://reddit.com/u/{chosen[1]}')
        embed.set_image(url = chosen[2])

        await ctx.send(embed = embed)


    @commands.command()
    async def meowIRL(self, ctx):
        posts = [[post.author, post.url] for post in reddit.subreddit("MEOW_IRL").hot(limit = self.limit)]
        posts = list(filter(lambda p: '.gif' in p[2], posts[1:])) # rem pinned and gifs

        chosen = random.choice(posts)

        embed = discord.Embed(title = "MEOW!")
        embed.set_author(name = f'u/{chosen[0]}', url = f'https://reddit.com/u/{chosen[0]}')
        embed.set_image(url = chosen[1])

        await ctx.send(embed = embed)


    @commands.command()
    async def showerthought(self, ctx):

        thoughts = [[thought.title, thought.author, thought.permalink] for thought in reddit.subreddit("showerthoughts").hot(limit = self.limit)]

        chosen = random.choice(thoughts)

        embed = discord.Embed(
            title = chosen[0],
            description = f'[Thought]({chosen[2]}) by [u/{chosen[1]}](https://reddit.com/u/{chosen[1]}) on [r/showerthoughts](https://reddit.com/r/showerthoughts)',
            color = self.showercolor
        )

        await ctx.send(embed = embed)


def setup(Client):
    Client.add_cog(subreddits(Client))
