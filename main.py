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

@Client.command()
async def hi(ctx, message):
    await ctx.message.channel.send("Hello, " + ctx.message.author.name + "!")


Client.run(os.getenv('BOT_TOKEN'))
