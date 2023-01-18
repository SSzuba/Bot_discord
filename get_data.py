from difflib import SequenceMatcher
from pysondb import db
from selenium import webdriver
from discord.ext import commands, tasks
from sites import sport_sites_list, business_sites_list, moto_sites_list


database = db.getDb("db.json")
databaseDet = db.getDb("details.json")
# for local usage
driver = webdriver.Chrome()
# for docker usage
# driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options=webdriver.ChromeOptions())

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
                                        if linkChecker == linkUrl:
                                            c = 1
                                        elif titleChecker == title:
                                            c = 1
                                    except:
                                        c = 0
                                if c == 0:
                                    database.add(item)
                                    await ctx.send("NEW! " + title + " " + linkUrl)
                                else:
                                    await asyncio.sleep(10)
                                    break
                except:
                    break
        

def get_article_details(type_name):
    infoTags = ['article', 'div', 'p', 'a', 'span']
    data = database.getByQuery({"type": type_name})
    dataCheck = databaseDet.getByQuery({"type": type_name})
    for d in range(len(data) - 1):
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
                            databaseDet.add(item)
                            counter += 1
                        else:
                            break
            except:
                break


async def check_for_updates(ctx):
    infoTags = ['article', 'div', 'p', 'a', 'span']
    data = databaseDet.getAll()
    for d in range(len(data) - 1):
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
