from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pysondb import db
import os
from sites import sites, sport_sites
from coockies import coockies_accept
from difflib import SequenceMatcher
import re
from datetime import datetime

os.remove("db.json")
database = db.getDb("db.json")
driver = webdriver.Chrome()
c = 1

def get_sport_articles():
    for s in sites_list:

        counter = 0

        driver.get(s)
        # driver.find_element_by_tag_name("body").send_keys(Keys.END)
        #buttons = driver.find_elements_by_tag_name("button")
        # coockies_accept(buttons)
        origin = driver.current_window_handle         
        articlesTags = ['h1', 'h2', 'h3', 'h4', 'a']
        timeTags = ['a', 'span', 'time']
        for t in articlesTags:
            try:
                driver.find_element_by_tag_name("body").send_keys(Keys.END)
                articles = driver.find_elements_by_tag_name(t)
                for a in articles:
                    title = str(a.text)
                    if title != '' and len(title) > 40 and counter < 5:
                        links = driver.find_elements_by_tag_name("a")
                        for l in links:
                            linkUrl = str(l.get_attribute('href'))
                            if linkUrl and SequenceMatcher(None, title, linkUrl).ratio() > 0.3 and counter < 5:
                                l.send_keys(Keys.CONTROL + Keys.RETURN)
                                driver.switch_to.window(driver.window_handles[c])
                                link = driver.current_url
                                counter2 = 0
                                for ti in timeTags:
                                    elements = driver.find_elements_by_tag_name(ti)
                                    time = ''
                                    try:
                                        for e in elements:
                                            reg = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
                                            time = re.search(reg, str(e.text))
                                            if time and counter2 < 1:
                                                item = {
                                                    "title": title,
                                                    "url": link,
                                                    "timeAdd": time.string,
                                                    "type": 'sport',
                                                    "site": s
                                                }
                                                database.add(item)
                                                counter += 1
                                                counter2 += 1
                                                c += 1
                                                driver.switch_to.window(driver.window_handles[0])

                                    except Exception as e:
                                        driver.switch_to.window(driver.window_handles[0])
                                        break
            except Exception as e:
                break
            c = 1


sites_list = []

for s in sites:
    sport_sites.append('sport.'+s)

for s in sport_sites:
    sites_list.append("https://" + s)
sites_list.reverse()
get_sport_articles()


driver.close()
driver.quit()

# akceptacje coockies tvp(pobieranie), wprost, ?interia?, wp(tytul)
