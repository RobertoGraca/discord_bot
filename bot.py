from discord.ext import commands
from consts import BOT_TOKEN
from youtube import get_link
from tenor import get_gif


bot = commands.Bot(command_prefix='->')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#-------------------------------------- TENOR -----------------------------------------------
@bot.command()
async def gif(ctx, *args):
    await get_gif(ctx,join_args('+',args))

#-------------------------------------- YOUTUBE ---------------------------------------------
@bot.command()
async def ytlink(ctx, *args):
    await ctx.send(get_link(join_args('+',args)))

#-------------------------------------- AUXILIAR --------------------------------------------
def join_args(separator,args):
    return separator.join(args)

bot.run(BOT_TOKEN)