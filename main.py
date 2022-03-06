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
import apis

load_dotenv()


i_prefix = '!' # change this
i_intents = discord.Intents.all()


Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

@Client.event
async def on_ready():
    for f in os.listdir('./cogs'):
    	if (f.endswith('.py') and not f.startswith('.')):
            Client.load_extension('cogs.' + f[:-3])

    for c in Client.cogs:
        print(f'loaded {c}')
    print('-'*10)
    print(':)')


Client.run(os.getenv('BOT_TOKEN'))
