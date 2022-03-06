#!/usr/bin/python3

import discord
from discord.ext import commands

class annoy(commands.Cog):
    def __init__(self, Client):
        self.Client = Client

        self.annoylist = set()
        self._im = ['im', 'i\'m', 'i am']


    @commands.Command(usage='(start|stop) @user')
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
            if any(list := [w in message.content.lower() for w in self._im]):
                present = [int(a) * b for a, b in zip(list, self._im)]
                present[:] = [x for x in present if x != '']
                msg = message.content.split(' ')[(message.content.split(' ').index(present[0])):]
                await message.channel.send(f'''Hi {' '.join(msg[1:])}, I\'m dad.''')
            else:
                await message.channel.send(''.join(random.choice((str.upper, str.lower)) for c in message.content.lower()))

def init(Client):
    Client.add_cog(annoy(Client))
