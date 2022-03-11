import discord
from discord.ext import commands, tasks
import ffmpeg
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
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

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist, add rest to queue
            queue.append(data['entries'])
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music(commands.Cog):
    def __init__(self, client):
        self.Client = client


    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await ctx.message.author.channel.connect()

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
        async with ctx.typing():
            if (not ctx.voice_client.is_playing()) or force:
                player = await YTDLSource.from_url(url, loop=self.Client.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(e) if e else None)
                await ctx.send(embed=discord.Embed(title=f'Now playing: {player.title}', description=player.channel, color=0xC4302B))
            elif not force:
                queue.append({'url': url})
                await ctx.send('Queued!')
            else:
                return


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
            await self.play(ctx, url=queue.pop(0)['url'], force=True)

    # WORK IN PROGRESS
    @commands.command()
    async def np(self, ctx):
        global queue
        if not ctx.voice_client.is_playing():
            return await ctx.send('Not currently playing anything.')
        else:
            await ctx.send(embed=discord.Embed(title=f'Now playing: {player.title}', description=player.channel, color=0xC4302B))

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
