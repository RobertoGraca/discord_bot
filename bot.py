from discord.ext import commands
import discord
from consts import BOT_TOKEN
from youtube import get_link, play_song, skip_song, stop_song
from tenor import get_gif

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='->', intents=intent)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# -------------------------------------- TENOR -----------------------------------------------


@bot.command()
async def gif(ctx, *args):
    await get_gif(ctx, join_args('+', args))

# -------------------------------------- YOUTUBE ---------------------------------------------


@bot.command()
async def search(ctx, *args):
    await ctx.send(get_link(join_args('+', args)))


@bot.command()
async def play(ctx, *args):
    await play_song(ctx, join_args('+', args), False)


@bot.command()
async def stop(ctx):
    await stop_song(ctx)


@bot.command()
async def skip(ctx):
    await skip_song(ctx)

# -------------------------------------- AUXILIAR --------------------------------------------


def join_args(separator, args):
    return separator.join(args)


bot.run(BOT_TOKEN)
