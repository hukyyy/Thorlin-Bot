#!/usr/bin/env python3

import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

i_prefix = '!' # change this
i_intents = discord.Intents.all()

Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

s_token = os.getenv('BOT_TOKEN') # hidden in .env file (git-ignored)

Client.run(os.getenv('BOT_TOKEN'))
