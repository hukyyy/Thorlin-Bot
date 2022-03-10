#!/usr/bin/python3
import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


i_prefix = '!' # change this
i_intents = discord.Intents.all()


Client = commands.Bot(command_prefix=commands.when_mentioned_or(i_prefix), intents=i_intents)

@Client.event
async def on_ready():
    for f in os.listdir('./cogs'):
    	if (f.endswith('.py') and not f.startswith('.')):
            Client.load_extension('cogs.' + f[:-3])

    for c in Client.cogs:
        print(f'loaded {c}')
    print('-'*10)
    print(':)')

if __name__ == '__main__':
    try:
        Client.run(os.getenv('BOT_TOKEN'))
    finally:
        for c in Client.cogs:
            Client.unload_extension(c)
