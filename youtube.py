import discord
import urllib.request
import re
import asyncio
from  yt_dlp import YoutubeDL
from consts import BOT_NAME

song_queue = {}


def get_link(args):
    url = f'https://www.youtube.com/results?search_query={args}'
    results = urllib.request.urlopen(url)
    if(results.getcode() != 200):
        print(f'HTTP Error {results.getcode()}')
        return
    video_id = re.findall(r"watch\?v=(\S{11})", results.read().decode())[0]
    result_url = f'https://www.youtube.com/watch?v={video_id}'

    return result_url


async def play_song(ctx, args, called_by_coroutine):
    if ctx.author.voice is None:
        await ctx.send('You need to be in a voice channel')
        return

    channel = ctx.author.voice.channel

    is_connected = False
    for member in channel.members:
        if member.bot and member.name == BOT_NAME:
            is_connected = True
            break

    if not is_connected:
        await channel.connect()

    voice_client = ctx.voice_client

    url = ''
    if not called_by_coroutine:
        if len(args) == 1 and 'https://www.youtube.com/watch?v=' in args:
            url = args
        else:
            url = get_link(args)
        song_queue[url] = ctx
    else:
        voice_client.stop()
        if len(song_queue) < 1:
            embed = discord.Embed(title=f'**No more songs to play**', colour=discord.Color.blue())
            await ctx.send(embed=embed)
            await voice_client.disconnect()
            return

    if voice_client.is_playing():

        YDL_OPTIONS = {'format': "bestaudio"}
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
        embed = discord.Embed(title=f'**Queued**', colour=discord.Color.blue(),
                              description=f'[{title}]({url})\nRequested by {ctx.author.mention}')
        embed.set_thumbnail(url=info['thumbnails'][0]['url'])
        embed.set_footer(text=f'Position #{len(song_queue)}')
        await ctx.send(embed=embed)
    else:
        YDL_OPTIONS = {'format': "bestaudio"}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        with YoutubeDL(YDL_OPTIONS) as ydl:
            url = next(iter(song_queue))

            info = ydl.extract_info(url, download=False)

            title = info['title']
            url2 = info['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, method='fallback')
            voice_client.play(source)

        embed = discord.Embed(title=f'**Now Playing**', colour=discord.Color.blue(),
                              description=f'[{title}]({url})\nRequested by {song_queue.get(url).author.mention}')
        embed.set_thumbnail(url=info['thumbnails'][len(info['thumbnails'])-1]['url'])
        await ctx.send(embed=embed)
        song_queue.pop(url)

        await next_song(ctx, info['duration'])


async def next_song(ctx, time):
    await asyncio.sleep(time+1)
    if len(song_queue) > 0:
        await play_song(ctx, '', True)


async def stop_song(ctx):
    if ctx.author.voice is None:
        await ctx.send('You need to be in a voice channel')
        return

    channel = ctx.author.voice.channel

    is_connected = False
    for member in channel.members:
        if member.bot and member.name == BOT_NAME:
            is_connected = True

    if is_connected:
        song_queue.clear()
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

        embed = discord.Embed(title=f'**Stopped music playback**', colour=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(title=f'**I need to be in a voice channel**', colour=discord.Color.blue())
        await ctx.send(embed=embed)
        return


async def skip_song(ctx):

    if ctx.author.voice is None:
        await ctx.send('You need to be in a voice channel')
        return

    channel = ctx.author.voice.channel

    is_connected = False
    for member in channel.members:
        if member.bot and member.name == 'Robinho':
            is_connected = True

    if not is_connected:
        await channel.connect()

    voice_client = ctx.voice_client

    embed = discord.Embed(title=f'**Skipped music**', colour=discord.Color.blue())
    await ctx.send(embed=embed)

    voice_client.stop()
    if len(song_queue) < 1:
        await ctx.send('No more songs to play')
        await voice_client.disconnect()
        return

    YDL_OPTIONS = {'format': "bestaudio"}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        url = next(iter(song_queue))

        info = ydl.extract_info(url, download=False)

        title = info['title']
        url2 = info['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, method='fallback')
        voice_client.play(source)

    embed = discord.Embed(title=f'**Now Playing**', colour=discord.Color.blue(),
                          description=f'[{title}]({url})\nRequested by {song_queue.get(url).author.mention}')
    embed.set_thumbnail(url=info['thumbnails'][len(info['thumbnails'])-1]['url'])
    await ctx.send(embed=embed)
    song_queue.pop(url)

    await next_song(ctx, info['duration'])
