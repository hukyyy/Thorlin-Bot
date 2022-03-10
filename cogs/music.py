import discord
from discord.ext import commands
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


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music(commands.Cog):
    def __init__(self, client):
        self.Client = client
        self.queue = []


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
    async def play(self, ctx, *, url: str):

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.Client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))


    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        await self.stop()
        await ctx.voice_client.disconnect()


    @play.before_invoke
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
