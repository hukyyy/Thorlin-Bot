#!/usr/bin/python3
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

load_dotenv()


i_prefix = '!' # change this
i_intents = discord.Intents.all()

# QOL
discord.ext.commands.DefaultHelpCommand.no_category = 'General'
discord.ext.commands.DefaultHelpCommand.sort_commands = False


Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

reddit = praw.Reddit(
client_id = os.getenv('REDDIT_CLIENT_ID'),
client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
refresh_token = os.getenv('REDDIT_REFRESH_TOKEN'),
user_agent = os.getenv('REDDIT_USER_AGENT')
)
reddit.read_only = True

@Client.event
async def on_ready():
    for f in os.listdir('./cogs'):
    	if f.endswith('.py'):
            Client.load_extension('cogs.' + f[:-3])
    print(':)')

    # for n, c in Client.cogs:
    #     print(j.get_commands())


Client.run(os.getenv('BOT_TOKEN'))
