from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pysondb import db
import os
from sites import sites, sport_sites
from coockies import coockies_accept
from difflib import SequenceMatcher

os.remove("db.json")
database = db.getDb("db.json")

driver = webdriver.Chrome()


def get_sport_articles():

    for s in sites_list:
        driver.get(s)
        driver.find_element_by_tag_name("body").send_keys(Keys.END)
        buttons = driver.find_elements_by_tag_name("button")
        coockies_accept(buttons)
        counter = 0
        tags = ['h1', 'h2', 'h3', 'h4']
        for t in tags:
            driver.find_element_by_tag_name("body").send_keys(Keys.END)
            articles = driver.find_elements_by_tag_name(t)
            for a in articles:
                title = str(a.text)
                if title != '' and len(title) > 20 and counter < 5:
                    print(len(title))
                    print(str(a.text))
                    links = driver.find_elements_by_tag_name("a")
                    for l in links:
                        linkUrl = str(l.get_attribute('href'))
                        if linkUrl and SequenceMatcher(None, title, linkUrl).ratio() > 0.33:
                            q = {"title": title}
                            data = database.getByQuery(query=q)
                            print(data)
                            print(linkUrl)
                            item = {
                                "title": title,
                                "url": linkUrl,
                                "type": 'sport',
                                "site": s
                            }
                            
                            if SequenceMatcher(None, data, item).ratio() < 0.5:
                                database.add(item)
                                counter += 1


sites_list = []

for s in sites:
    sport_sites.append('sport.'+s)

for s in sport_sites:
    sites_list.append("https://" + s)

get_sport_articles()


# driver.close()
# driver.quit()
