from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pysondb import db

database = db.getDb("db.json")

driver = webdriver.Chrome()


def get_articles(url, articlesType):
    counter = 0
    driver.get(url)

    articles = driver.find_elements_by_tag_name('h3')

    for a in articles:
        print(str(a.text))
        link = driver.find_element_by_link_text(str(a.text))
        print(str(link.get_attribute('href')))
        database.add({
            "title": str(a.text),
            "url": str(link.get_attribute('href')),
            "type": articlesType
        })
        counter += 1
        if counter > 30:
            exit()

    articles = driver.find_elements_by_tag_name('h4')

    for a in articles:
        if str(a.text) != "":
            print(str(a.text))
            link = driver.find_element_by_link_text(str(a.text))
            print(str(link.get_attribute('href')))
            database.add({
                "title": str(a.text),
                "url": str(link.get_attribute('href')),
                "type": articlesType
            })


# artykuły ogólnej tematyki
get_articles(
    "https://news.google.com/topstories?hl=pl&gl=PL&ceid=PL:pl", "general")

# spersonalizowane tematy
search_title = "wiadomości sportowe z piłki nożnej"
search_title.replace(" ", "%20")
custom_url = "https://news.google.com/search?q=" + \
    search_title + "&hl=pl&gl=PL&ceid=PL%3Apl"
get_articles(custom_url, search_title)

driver.close()
driver.quit()
