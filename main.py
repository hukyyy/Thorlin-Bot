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
    Client.load_extension('cogs.adventurecat-cog')
    Client.load_extension('cogs.hi-cog')
    Client.load_extension('cogs.showerthought-cog')
    Client.load_extension('cogs.annoy-cog')
    Client.load_extension('cogs.chemquiz-cog')
    Client.load_extension('cogs.meowIRL-cog')
    Client.load_extension('cogs.eyebleach-cog')
    print(':)')


Client.run(os.getenv('BOT_TOKEN'))
