#!/usr/bin/env python3

import discord
import discord.ext.commands
import discord.ext.tasks

import asyncio
import os

i_prefix = '!' # change this
i_intents = Intents.all()

Client = commands.Bot(command_prefix=i_prefix, intents=i_intents)









s_token = os.environ.get('BOT_TOKEN') # set an env variable -> export BOT_TOKEN='super sekrit token' <- or somethin

await Client.login(token=s_token, bot=True)
await Client.connect(reconnect=True)
