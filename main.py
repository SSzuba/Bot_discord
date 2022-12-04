import os
import discord
import use_data
from discord.ext import commands

TOKEN = 'OTYxOTIyMzI4MDAwODg0NzM3.G3DcYT.ArU5lRWsFaD5cs4YWU75tT-F8cix_NRdpNPBGM'

bot = commands.Bot(command_prefix="!")


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


@bot.command()
async def szukaj(ctx, *args):
    arguments = ' '.join(args)
    msg = use_data.get_articles_by_title(arguments)
    await ctx.send(str(msg))

bot.run(TOKEN)
