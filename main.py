#!/usr/bin/env python3

import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


i_prefix = '!' # change this
i_intents = Intents.all()

Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

# bot code

s_token = os.getenv('BOT_TOKEN') # hidden in .env file (git-ignored)

await Client.login(token=s_token, bot=True)
await Client.connect(reconnect=True)
