import sqlite3
from difflib import SequenceMatcher
from selenium import webdriver
from discord.ext import commands, tasks
from datetime import datetime

con = sqlite3.connect("database.db")
cur = con.cursor()
# for local usage
driver = webdriver.Chrome()
# for docker usage
# driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options=webdriver.ChromeOptions())


def get_articles(type):
    res = cur.execute('SELECT url, type FROM sites WHERE type = ?', (type,))
    sites = []
    for row in res.fetchall():
        url = row[0]
        sites.append(url)
    for s in sites:
        driver.get(s)
        articlesTags = ['h1', 'h2', 'h3', 'h4', 'a']
        linkChecker = ''
        titleChecker = ''
        founded = False
        for t in articlesTags:
            articles = driver.find_elements_by_tag_name(t)
            for a in articles:
                try:
                    title = str(a.text)
                    if title != '' and len(title) > 50:
                        links = driver.find_elements_by_tag_name("a")
                        for l in links:
                            linkUrl = str(l.get_attribute('href'))
                            res = cur.execute('SELECT title, url FROM articles WHERE type = ?', (type,))
                            if len(linkUrl) > 50 and SequenceMatcher(None, title, linkUrl).ratio() > 0.3:
                                founded = False
                                for row in res.fetchall():
                                    titleChecker = row[0]
                                    linkChecker = row[1]
                                    if linkChecker == linkUrl or titleChecker == title:
                                        founded = True
                                if founded is False:
                                    now = datetime.now()
                                    date = now.strftime("%d/%m/%Y %H:%M:%S")
                                    res2 = cur.execute(
                                        f'INSERT INTO articles(title, url, details, type, date, status) VALUES(?, ?, ?, ?, ?, ?)', (title, linkUrl, "det", type, date, "New"))
                                    con.commit()
                                else:
                                    break
                except:
                    break



def get_article_details(type):
    infoTags = ['article', 'div', 'p', 'a', 'span']
    res = cur.execute('SELECT title, url, details FROM articles WHERE type = ?', (type,))
    for row in res.fetchall():
        added = False
        title = row[0]
        url = row[1]
        details = row[2]
        if details == "det":
            try:
                driver.get(url)
                for t in infoTags:
                    elements = driver.find_elements_by_tag_name(t)
                    for e in elements:
                        if added is False and len(e.text) > 500:
                            details = str(e.text)[0:1000]
                            res2 = cur.execute(
                                'UPDATE articles SET details = ? WHERE title = ? AND url = ? AND type = ?', (details, title, url, type))
                            con.commit()
                            added = True
                        elif added is True:
                            break
            except:
              break


def check_for_updates():
    infoTags = ['article', 'div', 'p', 'a', 'span']
    res = cur.execute(
        'SELECT title, url, details FROM articles')
    for row in res.fetchall():
        changed = False
        title = row[0]
        url = row[1]
        details = row[2]
        driver.get(url)
        for t in infoTags:
            try:
                elements = driver.find_elements_by_tag_name(t)
                for e in elements:
                    newDetails = str(e.text)[0:1000]
                    if changed is False and len(e.text) > 500 and details != newDetails:
                        now = datetime.now()
                        date = now.strftime("%d/%m/%Y %H:%M:%S")
                        res2 = cur.execute(
                            'UPDATE articles SET details = ?, status = "Update", date = ? WHERE title = ? AND url = ?', (newDetails, date, title, url))
                        con.commit()
                        changed = True
                    elif changed is True:
                        break
            except:
                break

while True:
    #get_articles("sport")
    #get_article_details("sport")  
    #get_articles("biznes")
    # get_article_details("biznes")
    # get_articles("moto")
    # get_article_details("moto")
    check_for_updates()

