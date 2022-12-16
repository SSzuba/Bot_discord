import os
import discord
import use_data
import get_data
from discord.ext import commands

TOKEN = 'OTYxOTIyMzI4MDAwODg0NzM3.GwNZZq.lynrZbGfi1uk-lVEFyKIdTZAQO5BYAXDg3rT00'

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")


@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


@bot.command()
async def sport(ctx):
    msg = use_data.get_articles('sport')
    await ctx.send(str(msg))


@bot.command()
async def biznes(ctx):
    msg = use_data.get_articles('biznes')
    await ctx.send(str(msg))


@bot.command()
async def motoryzacja(ctx):
    msg = use_data.get_articles('moto')
    await ctx.send(str(msg))
    

# @bot.command()
# async def szukaj(ctx, *args):
#     arguments = ' '.join(args)
#     msg = use_data.get_articles_by_title(arguments)
#     await ctx.send(str(msg))

bot.run(TOKEN)
