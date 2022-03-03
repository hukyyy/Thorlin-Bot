#!/usr/bin/env python3

import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import os
import praw
import random
from dotenv import load_dotenv


load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('REDDIT_CLIENT_ID'),
    client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
    refresh_token = os.getenv('REDDIT_REFRESH_TOKEN'),
    user_agent = os.getenv('REDDIT_USER_AGENT'),
)

reddit.read_only = True

i_prefix = '!' # change this
i_intents = discord.Intents.all()

Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

@Client.command()
async def hi(ctx):
    await ctx.message.channel.send(f"Hello, {ctx.message.author.name}!")


# Imporvements necessary :
# - Filter image posts
# - Handle image galleries
@Client.command()
async def adventurecat(ctx):
    posts = []
    for post in reddit.subreddit("adventurecats").hot(limit = 10):
        posts.append([post.title, post.author, post.url, post.permalink])

    chosen = random.choice(posts)
    await ctx.message.channel.send(chosen[2])


Client.run(os.getenv('BOT_TOKEN'))
