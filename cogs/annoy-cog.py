#!/usr/bin/python3

import discord
from discord.ext import commands
import random

class annoy(commands.Cog):
    def __init__(self, Client):
        self.Client = Client

        self.annoylist = set()
        self._im = ['im', 'i\'m', 'i am']
        print(*self._im)


    @commands.command(usage='(start|stop) @user')
    async def annoy(self, ctx, op='start'):
        if (op.lower() == 'start'):
            self.annoylist.add(ctx.message.mentions[0])
        elif (op.lower() == 'stop'):
            self.annoylist.remove(ctx.message.mentions[0])
        else:
            await ctx.send('Didn\'t quite get that :b')

    @commands.Cog.listener('on_message')
    async def _annoy(self, message):
        if (not message.content.startswith('!') and message.author in self.annoylist):
            list = [w in message.content.lower() for w in self._im]
            if any(list):
                text = message.content.lower().replace('i am', 'im').replace('i\'m', 'im')
                msg = message.content.split(' ')[(text.lower().split(' ').index('im')):]
                await message.channel.send(f'''Hi {' '.join(msg[1:])}, I\'m dad.''')
            else:
                await message.channel.send(''.join(random.choice((str.upper, str.lower))(c) for c in message.content.lower()))

def setup(Client):
    Client.add_cog(annoy(Client))
