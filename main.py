#!/usr/bin/env python3

import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import os
import re
import praw
import random
import requests
from dotenv import load_dotenv


load_dotenv()

i_prefix = '!' # change this
i_intents = discord.Intents.all()

_im = ['im', 'i\'m', 'i am']
annoylist = set()

Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

reddit = praw.Reddit(
client_id = os.getenv('REDDIT_CLIENT_ID'),
client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
refresh_token = os.getenv('REDDIT_REFRESH_TOKEN'),
user_agent = os.getenv('REDDIT_USER_AGENT'),
)
reddit.read_only = True


@Client.command()
async def hi(ctx):
    await ctx.message.channel.send(f"Hello, {ctx.message.author.name}!")

# Imporvements necessary :
# - Filter image posts
# - Handle image galleries
@Client.command()
async def adventurecat(ctx):
    posts = [[post.title, post.author, post.url, post.permalink] for post in reddit.subreddit("adventurecats").hot(limit = 50)]

    images = list(filter(lambda p: 'i.redd.it' in p[2], posts))
    # galleries = list(filter(lambda p: 'gallery' in p[2], posts))
    #
    # if galleries:
    #     s = requests.Session()
    #     s.headers.update({'User-Agent': 'Thorlin-Bot'})
    #     imglinks = [re.search(r'https:\/\/preview.redd.it\/[a-z0-9]{13}\.jpg', s.get(galleries[i][2]).text).group() for i in range(len(galleries))]
    #     images += imglinks

    await ctx.message.channel.send(random.choice(images[2]))

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

@Client.command()
async def annoy(ctx, op='start'):
    f'''Annoys a pinged user: {i_prefix}annoy (start|stop) \@user'''
    global annoylist
    if (op.lower() == 'start'):
        annoylist.add(ctx.message.mentions[0])
    elif (op.lower() == 'stop'):
        annoylist.remove(ctx.message.mentions[0])
    else:
        ctx.send('Didn\'t quite get that :b')

@Client.listen('on_message')
async def _annoy(message):
    global annoylist
    print(message.content, message.author, *annoylist)
    if message.author in annoylist:
        if any(list := (w in message.content.lower() for w in _im)):
            present = [a * b for a, b in zip(list, _im)]
            msg = message.content.split(' ')[(message.content.split(' ').index(present[0]))]
            message.channel.send(f'''Hi {' '.join(msg)}, I\'m dad.''')
        else:
            message.channel.send(''.join(random.choice((str.upper, str.lower))(c) for c in message.content.lower()))

Client.run(os.getenv('BOT_TOKEN'))
