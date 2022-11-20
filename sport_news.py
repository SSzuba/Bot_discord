import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from coockies import coockies_accept
from pysondb import db
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sites import sites, sport_sites

database = db.getDb("db.json")
databaseD = db.getDb("details.json")
driver = webdriver.Chrome()

def get_sport_articles():
    database = db.getDb("db.json")
    for s in sites_list:
        driver.get(s)
        articlesTags = ['h1', 'h2', 'h3', 'h4', 'a']
        linkChecker = ''
        titleChecker = ''
        counter = 0
        driver.find_element_by_tag_name("body").send_keys(Keys.END)
        for t in articlesTags:
            articles = driver.find_elements_by_tag_name(t)
            for a in articles:
                try:
                    title = str(a.text)
                    if title != '' and len(title) > 40 and counter < 5:
                        links = driver.find_elements_by_tag_name("a")
                        for l in links:
                            linkUrl = str(l.get_attribute('href'))
                            data = database.getByQuery({"title": title})
                            if linkUrl and SequenceMatcher(None, title, linkUrl).ratio() > 0.3 and counter < 5:
                                item = {
                                    "title": title,
                                    "url": linkUrl,
                                    "type": 'sport'
                                }
                                if linkChecker != linkUrl and titleChecker != title and counter < 5 and data == []:
                                    database.add(item)
                                    counter += 1
                                    linkChecker = linkUrl
                                    titleChecker = title
                                    data = ''
                                else:
                                    break
                except:
                    break
    


def get_article_details():
    databaseD = db.getDb("details.json")
    infoTags = ['div', 'span', 'p']
    data = database.getByQuery({"type": 'sport'})
    infoChecker = ''
    for d in range(len(data)):
        counter = 0
        url = data[d]["url"]
        title = data[d]["title"]
        driver.get(url)
        for t in infoTags:
            elements = driver.find_elements_by_tag_name(t)
            for e in elements:
                dataCheck = databaseD.getAll()
                for check in range(len(dataCheck)):
                    infoChecker = dataCheck[check]['info']
                    if counter < 1 and len(e.text) > 300 and e.text != infoChecker:
                        item = {
                            "title": title,
                            "url": url,
                            "info": e.text,
                            "type": 'sport'
                        }
                        databaseD.add(item)
                        counter += 1
                    else:
                        break



sites_list = []

for s in sites:
    sport_sites.append('sport.'+s)

for s in sport_sites:
    sites_list.append("https://" + s)

#get_sport_articles()
get_article_details()

driver.close()
driver.quit()
