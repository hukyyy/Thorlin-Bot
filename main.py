#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import random
import os
from dotenv import load_dotenv

from orgachem import OrgaChem


# easily accessible important things
i_prefix = '!' # change this
i_intents = discord.Intents.all()

# QOL
discord.ext.commands.DefaultHelpCommand.no_category = 'General'
discord.ext.commands.DefaultHelpCommand.sort_commands = False


Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)

@Client.event
async def on_ready():
    load_dotenv()
    print(':)')

@Client.command()
async def hi(ctx, message):
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

<<<<<<< HEAD
Client.run(os.getenv('BOT_TOKEN'))
=======

Client.run(token=os.getenv('BOT_TOKEN'), bot=True)
>>>>>>> dev
