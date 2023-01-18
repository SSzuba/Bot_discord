import discord
import use_data
from get_data import get_articles, get_article_details, check_for_updates
from difflib import SequenceMatcher
from pysondb import db
from selenium import webdriver
from discord.ext import commands, tasks
from sites import sport_sites_list, business_sites_list, moto_sites_list

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


@bot.command()
async def follow(ctx):
    try:
        while(True):
            await get_articles(sport_sites_list, 'sport', ctx)
            get_article_details('sport')
            await get_articles(moto_sites_list, 'moto', ctx)
            get_article_details('moto')
            await get_articles(business_sites_list, 'biznes', ctx) 
            get_article_details('biznes')
            await check_for_updates(ctx)
    except:
        await ctx.send('ERROR! Please repeat command !follow')

bot.run(TOKEN)
