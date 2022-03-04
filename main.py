#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import random
import os
import re
import praw
import random
import requests
from dotenv import load_dotenv

from orgachem import OrgaChem


# easily accessible important things

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

# QOL
discord.ext.commands.DefaultHelpCommand.no_category = 'General'
discord.ext.commands.DefaultHelpCommand.sort_commands = False


Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

load_dotenv()

@Client.event
async def on_ready():
    print(':)')

@Client.command()
async def hi(ctx):
    await ctx.message.channel.send(f"Hello, {ctx.message.author.name}!")

@Client.command()
async def chemquiz(ctx):

    keys = list(vars(OrgaChem()).keys())
    values = list(vars(OrgaChem()).values())

    await ctx.message.channel.send(f'What\'s this functional group called?\n{values[(n := random.randint(0, len(values)))]}')

    reply = await Client.wait_for('message', check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel)

    if reply.content.lower() == (a := keys[n].lower()):
        await ctx.message.channel.send(f'Yep! Answer was \'{a}\'')
    else:
        await ctx.message.channel.send(f'Noooooooo.. Answer was \'{a}\'')

# !adventurecat TODO
# - Handle Image galleries
# - Filter Image posts from Text posts
# - Make it an embed!

# @Client.command()
# async def adventurecat(ctx):
#     posts = [[post.title, post.author, post.url, post.permalink] for post in reddit.subreddit("adventurecats").hot(limit = 50)]
#
#     images = list(filter(lambda p: 'i.redd.it' in p[2], posts))
#     # galleries = list(filter(lambda p: 'gallery' in p[2], posts))
#     #
#     # if galleries:
#     #     s = requests.Session()
#     #     s.headers.update({'User-Agent': 'sex'})
#     #     imglinks = [re.search(r'https:\/\/preview.redd.it\/[a-z0-9]{13}\.jpg', s.get(galleries[i][2]).text).group() for i in range(len(galleries))]
#     #     images += imglinks
#
#     await ctx.message.channel.send(random.choice(images[2]))

@Client.command()
async def showerthought(ctx):
    thoughts = [[thought.title, thought.author, thought.permalink] for thought in reddit.subreddit("showerthoughts").hot(limit = 50)]

    chosen = random.choice(thoughts)

    embed = discord.Embed(
        title = chosen[0],
        description = f'[Thought]({chosen[2]}) by [u/{chosen[1]}](https://reddit.com/u/{chosen[1]}) on [r/showerthoughts](https://reddit.com/r/showerthoughts)',
        color = 0xd4f1f9
    )

    await ctx.message.channel.send(embed = embed)


Client.run(os.getenv('BOT_TOKEN'))
