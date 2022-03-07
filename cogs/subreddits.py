#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import asyncpraw

class subreddits(commands.Cog):

    def __init__(self, Client):
        self.Client = Client

        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.refresh_token = os.getenv('REDDIT_REFRESH_TOKEN')
        self.user_agent = os.getenv('REDDIT_USER_AGENT')

        # self.reddit = asyncpraw.Reddit(
        # client_id = os.getenv('REDDIT_CLIENT_ID'),
        # client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
        # refresh_token = os.getenv('REDDIT_REFRESH_TOKEN'),
        # user_agent = os.getenv('REDDIT_USER_AGENT'),
        # )
        # self.reddit.read_only = True

        self.limit = 50 # hot limit
        self.showercolor = 0xd4f1f9

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.reddit.close()



    @commands.command()
    async def adventurecat(self, ctx):
        async with asyncpraw.Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        refresh_token=self.refresh_token,
        user_agent=self.user_agent) as reddit:

            self.reddit.read_only = True
            subreddit = await reddit.subreddit('adventurecats', fetch=True)
            posts = []

            async for post in subreddit.hot(limit = self.limit):
                posts.append([post.title, post.author, post.url, post.permalink])

            images = list(filter(lambda p: 'i.' in p[2][:15], posts))

            await ctx.send(random.choice(images)[2])

        # Improvements necessary :
        #-------------------------
        # - Filter image posts
        # - Handle image galleries

        # OLD BROKEN CODE:
        #-----------------
        # galleries = list(filter(lambda p: 'gallery' in p[2], posts))
        # if galleries:
        #     s = requests.Session()
        #     s.headers.update({'User-Agent': 'Thorlin-Bot'})
        #     imglinks = [re.search(r'https:\/\/preview.redd.it\/[a-z0-9]{13}\.jpg', s.get(galleries[i][2]).text).group() for i in range(len(galleries))]
        #     images += imglinks


    @commands.command()
    async def eyebleach(self, ctx):
        async with asyncpraw.Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        refresh_token=self.refresh_token,
        user_agent=self.user_agent) as reddit:

            self.reddit.read_only = True

            subreddit = await self.reddit.subreddit('eyebleach', fetch=True)
            posts = []

            async for post in subreddit.hot(limit = self.limit):
                posts.append([post.title, post.author, post.url])

            posts = list(filter(lambda p: not ('.gif' in p[2]), posts[1:]))

            chosen = random.choice(posts)

            embed = discord.Embed(title = chosen[0])
            embed.set_author(name = f'u/{chosen[1]}', url = f'https://reddit.com/u/{chosen[1]}')
            embed.set_image(url = chosen[2] + '.gif' if not chosen[2].endswith('.gif') else chosen[2])
            await ctx.send(embed = embed)


    @commands.command()
    async def meowIRL(self, ctx):
        async with asyncpraw.Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        refresh_token=self.refresh_token,
        user_agent=self.user_agent) as reddit:

            self.reddit.read_only = True

            subreddit = await self.reddit.subreddit('MEOW_IRL', fetch=True)
            posts = []

            async for post in subreddit.hot(limit = self.limit):
                posts.append([post.author, post.url])

            chosen = random.choice(posts)

            embed = discord.Embed(title = 'MEOW!')
            embed.set_author(name = f'u/{chosen[0]}', url = f'https://reddit.com/u/{chosen[0]}')
            embed.set_image(url = (link := chosen[1] + '.gif' if (not chosen[1].endswith('.gif') and not 'i.redd.it' in chosen[1]) else chosen[1]))
            await ctx.send(embed = embed)


    @commands.command()
    async def showerthought(self, ctx):
        async with asyncpraw.Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        refresh_token=self.refresh_token,
        user_agent=self.user_agent) as reddit:

            self.reddit.read_only = True

            subreddit = await self.reddit.subreddit('showerthoughts', fetch=True)
            posts = []

            async for post in subreddit.hot(limit = self.limit):
                posts.append([post.title, post.author, post.permalink])

            chosen = random.choice(posts)

            embed = discord.Embed(
            title = chosen[0],
            description = f'[Thought]({chosen[2]}) by [u/{chosen[1]}](https://reddit.com/u/{chosen[1]}) on [r/showerthoughts](https://self.reddit.com/r/showerthoughts)',
            color = self.showercolor
            )

            await ctx.send(embed = embed)


def setup(Client):
    Client.add_cog(subreddits(Client))
