import asyncio
import discord
from discord.ext import commands, tasks
import ffmpeg
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

def red(m):
    return f'\u001b[31m{m}\u001b[0m'

ytdl_format_options = {
    'format': 'bestaudio',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

queue = []

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.channel = data.get('channel')
        self.url = data.get('url')
        self.channel_url = data.get('channel_url')
        self.thumbnail = data.get('thumbnail')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        global queue
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist, add rest to queue
            queue.append(data['entries'][1:10])
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @classmethod
    async def fill_thumbs(cls, *, loop=None):
        global queue
        loop = loop or asyncio.get_event_loop()

        for i in queue:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(i['url'], download=False))
            keys = i.keys()

            for e in ['title', 'channel', 'channel_url', 'thumbnail', 'duration']:
                if not e in keys:
                    i[e] = data.get(e)



class music(commands.Cog):
    def __init__(self, client):
        self.Client = client
        self.playing = {}


    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)
        await ctx.author.voice.channel.connect()

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        global queue
        await self.stop(ctx)
        await ctx.voice_client.disconnect()
        queue = []

    @commands.command()
    async def stop(self, ctx):
        global queue
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            queue = []

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, url: str, force = False):
        global queue
        print(ctx)
        async with ctx.typing():
            if (not ctx.voice_client.is_playing()) or force:
                player = await YTDLSource.from_url(url, loop=self.Client.loop, stream=True)
                # ctx.voice_client.play(player)
                ctx.voice_client.play(player, after=self.play_after)
                await ctx.send(embed=discord.Embed(title=f'Now playing: {player.title}', description=f'[{player.channel}]({player.channel_url})', color=0xC4302B))
                self.playing = {'url': url, 'title': player.title, 'channel': player.channel, 'channel_url': player.channel_url, 'thumbnail': player.thumbnail}
                print(red([(i, self.playing.get(i)) for i in self.playing.keys()]))
            elif not force:
                queue.append({'url': url})
                await ctx.send('Queued!')
                await YTDLSource.fill_thumbs(loop=self.Client.loop)
                print(red([i for i in queue]))
            else:
                return

    def play_after(self, ctx):
        coro = self.shortskip(ctx)
        fut = asyncio.run_coroutine_threadsafe(coro, self.Client.loop)
        try:
            fut.result()
        except Exception as ex:
            print(red(ex))
            pass

    async def shortskip(self, ctx):
        global queue
        self.playing = queue.pop(0)
        await self.play(ctx, url=self.playing['url'], force=True)

    @commands.command(aliases=['s'])
    async def skip(self, ctx, pos: int = 1):
        global queue
        if not ctx.voice_client.is_playing():
            await ctx.send('Not currently playing anything.')

        elif not queue:
            ctx.voice_client.stop()

        else:
            queue = queue[pos-1:]
            ctx.voice_client.stop()
            self.playing = queue.pop(0)
            await self.play(ctx, url=self.playing['url'], force=True)

    # WORK IN PROGRESS
    @commands.command()
    async def np(self, ctx):
        if ctx.voice_client.is_playing():
            print(red([(i, self.playing.get(i)) for i in self.playing.keys()]))
            await ctx.send(embed=discord.Embed(title=f'''Now playing: {self.playing.get('title')}''', description=f'''[{self.playing.get('channel')}]({self.playing.get('channel_url')})''', color=0xC4302B).set_image(self.playing.get('thumbnail').split('?')[0]))
        else:
            return await ctx.send('Not currently playing anything.')

    @play.before_invoke
    @skip.before_invoke
    @np.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')

def setup(Client):
    Client.add_cog(music(Client))
