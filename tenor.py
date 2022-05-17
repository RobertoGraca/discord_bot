from consts import API_TENOR_GIF_KEY,MY_MENTION
import requests
import discord
import random

async def get_gif(ctx, args):
    result = requests.get(f'https://g.tenor.com/v1/search?key={API_TENOR_GIF_KEY}&q={args}&media_filter=minimal')

    if result.status_code != 200:
        print(f'Could not retrieve GIF.\nHTTP Error {str(result.status_code)}')

    id = random.randint(0,19)

    i = 0
    url = ''
    for node in result.json()['results']:
        if i == id:
            try:
                url = node['media'][0]['gif']['url']
            except Exception:
                try:
                    url = node['media'][0]['mp4']['url']
                except Exception:
                    url = node['media'][0]['tinygif']['url']
            break
        i += 1

    embed = discord.Embed(title=f'Search Results', colour=discord.Color.orange(),description=f'Requested by {ctx.author.mention}')
    embed.set_footer(text='Provided by Tenor API',icon_url='https://i.ibb.co/dKtMKmG/tenor-logo.jpg')
    embed.set_image(url=url)
    await ctx.send(embed=embed)
