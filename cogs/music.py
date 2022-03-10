import discord
from discord.ext import commands
import ffmpeg
from pytube import YouTube, Search, Playlist

class music(commands.Cog):
    def __init__(self, client):
        self.Client = client
        self.queue = []

    async def get_stream(self, link: str, abr: int):

        yt = YouTube(link)

        audiostreams = yt.streams.filter(only_audio=True)
        bitrates = [int(s.abr.replace('kbps', '')) for s in audiostreams]

        closestbr = min(bitrates, key=lambda x:abs(x-abr))

        PCMStream = discord.FFmpegPCMAudio(
        source = yt.streams.filter(only_audio=True, abr=f'{closestbr}kbps')[0].url,
        options = f'-b:a {closestbr}K')

        return yt, PCMStream


    @commands.command()
    async def join(self, ctx):

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await ctx.message.author.channel.connect()


    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()


    @commands.command(aliases=['p'])
    async def play(self, ctx, *, link: str):

        if not 'www.' in link:
            ctx.send('Not a link! Please use !search or !s')
            return

        yt, PCMStream = await self.get_stream(link, ctx.voice_client.channel.bitrate)

        title = yt.title
        thumbnail_url = yt.thumbnail_url

        ctx.voice_client.play(PCMStream, after=lambda e: print('Player error: %s' % e) if e else None)

        embed = discord.Embed(title = f'Playing {yt.title}!', color=0xc4302b)
        embed.set_thumbnail(url = thumbnail_url)
        await ctx.send(embed=embed, delete_after=30)


    @commands.command(aliases=['s'])
    async def search(self, ctx, *, query):
        s = Search(query)
        # filter(s.results, lambda s: s.length != 0)

        activesearch = []

        embed=discord.Embed(title=f'Search reults for: {query}', url=f'''https://www.youtube.com/results?search_query={query.replace(' ', '+')}''', color=0xc4302b)
        embed.set_thumbnail(url=s.results[0].thumbnail_url)
        embed.add_field(name=s.results[0].title, value=s.results[0].author, inline=False)
        m = await ctx.send(embed=embed, delete_after=30)
        await m.add_reaction('✅')

        activesearch.append(m)

        for i in s.results[1:5]:
            embed=discord.Embed(color=0xc4302b)
            embed.set_thumbnail(url=i.thumbnail_url)
            embed.add_field(name=i.title, value=i.author, inline=False)
            m = await ctx.send(embed=embed, delete_after=30)
            await m.add_reaction('✅')
            activesearch.append(m)

        reacted = await self.Client.wait_for(
        event = 'reaction_add',
        check = lambda r, u: u == ctx.author and r.message in activesearch,
        timeout = 30
        )
        song = activesearch.index(reacted[0].message)

        yt = s.results[song]

        audiostreams = yt.streams.filter(only_audio=True)
        bitrates = [int(s.abr.replace('kbps', '')) for s in audiostreams]

        closestbr = min(bitrates, key=lambda x:abs(x-ctx.voice_client.channel.bitrate))

        PCMStream = discord.FFmpegPCMAudio(
        source = yt.streams.filter(only_audio=True, abr=f'{closestbr}kbps')[0].url,
        options = f'-b:a {closestbr}K')

        title = yt.title
        thumbnail_url = yt.thumbnail_url

        ctx.voice_client.play(PCMStream, after=lambda e: print('Player error: %s' % e) if e else None)

        embed = discord.Embed(title = f'Playing {yt.title}!', description=yt.author, color=0xc4302b)
        embed.set_thumbnail(url = thumbnail_url)
        await ctx.send(embed=embed, delete_after=30)


    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        await self.stop()
        await ctx.voice_client.disconnect()


    @play.before_invoke
    @search.before_invoke
    @leave.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(Client):
    Client.add_cog(music(Client))
