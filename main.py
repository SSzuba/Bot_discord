import os
import discord
import use_data
from difflib import SequenceMatcher
from pysondb import db
from selenium import webdriver
from discord.ext import commands, tasks
from sites import sport_sites_list, business_sites_list, moto_sites_list

TOKEN = 'OTYxOTIyMzI4MDAwODg0NzM3.GwNZZq.lynrZbGfi1uk-lVEFyKIdTZAQO5BYAXDg3rT00'

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
database = db.getDb("db.json")
databaseDet = db.getDb("details.json")
driver = webdriver.Chrome()

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
    while(True):
        await get_articles(sport_sites_list, 'sport', ctx)
        get_article_details('sport')
        await get_articles(moto_sites_list, 'moto', ctx)
        get_article_details('moto')
        await get_articles(business_sites_list, 'biznes', ctx) 
        get_article_details('biznes')
        await check_for_updates(ctx)

async def get_articles(list_name, type_name, ctx):
    for s in list_name:
        driver.get(s)
        articlesTags = ['h1', 'h2', 'h3', 'h4', 'a']
        linkChecker = ''
        titleChecker = ''
        c = 0
        for t in articlesTags:
            articles = driver.find_elements_by_tag_name(t)
            for a in articles:        
                try:
                    title = str(a.text)
                    if title != '' and len(title) > 50:
                        links = driver.find_elements_by_tag_name("a")
                        for l in links:
                            linkUrl = str(l.get_attribute('href'))
                            data = database.getAll()
                            if len(linkUrl) > 50 and SequenceMatcher(None, title, linkUrl).ratio() > 0.3:
                                item = {
                                    "title": title,
                                    "url": linkUrl,
                                    "type": type_name
                                }
                                for d in range(len(data)):
                                    linkChecker = data[d]["url"]
                                    titleChecker = data[d]["title"]
                                    try:
                                        if linkChecker == linkUrl and SequenceMatcher(None, linkChecker, linkUrl).ratio() > 0.3:
                                            c = 1
                                        elif titleChecker == title and SequenceMatcher(None, titleChecker, title).ratio() > 0.3:
                                            c = 1
                                    except:
                                        c = 0
                                if c == 0:
                                    database.add(item)
                                    await ctx.send("NEW! " + title + " " + linkUrl)
                                else:
                                    c = 0
                                    break
                except:
                    break

def get_article_details(type_name):
    infoTags = ['article', 'div', 'p', 'a', 'span']
    data = database.getByQuery({"type": type_name})
    dataCheck = databaseDet.getByQuery({"type": type_name})
    for d in range(len(data)):
        c = 0
        counter = 0
        url = data[d]["url"]
        title = data[d]["title"]
        try:
            if str(dataCheck[d]["url"]) == url:
                c = 1
        except:
            c = 0
        if c == 0:
            try:
                driver.get(url)
                for t in infoTags:
                    elements = driver.find_elements_by_tag_name(t)
                    for e in elements:
                        if counter < 1 and len(e.text) > 500:
                            item = {
                                "title": title,
                                "url": url,
                                "info": str(e.text)[0:1000],
                                "type": type_name
                            }
                            databaseD.add(item)
                            counter += 1
                        else:
                            break
            except:
                break


async def check_for_updates(ctx):
    infoTags = ['article', 'div', 'p', 'a', 'span']
    data = databaseDet.getAll()
    for d in range(len(data)):
        counter = 0
        url = data[d]['url']
        title = data[d]['title']
        infoChecker = data[d]['info']
        driver.get(url)
        for t in infoTags:
            try:
                elements = driver.find_elements_by_tag_name(t)
                for e in elements:
                    for check in range(len(data)):
                        if counter < 1 and len(e.text) > 500 and infoChecker != str(e.text)[0:1000]:
                            dataId = data[d]['id']
                            databaseDet.updateById(dataId,{"info":str(e.text)[0:1000]})
                            await ctx.send("UPDATE! " + title + " " + url)
                            counter += 1
                        else:
                            break
            except:
                break

# @bot.command()
# async def szukaj(ctx, *args):
#     arguments = ' '.join(args)
#     msg = use_data.get_articles_by_title(arguments)
#     await ctx.send(str(msg))

bot.run(TOKEN)
