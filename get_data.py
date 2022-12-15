from difflib import SequenceMatcher
from pysondb import db
from selenium import webdriver
from sites import sport_sites_list, business_sites_list, moto_sites_list
from redis import Redis
from rq import Queue
from apscheduler.schedulers.background import BackgroundScheduler

q = Queue(connection=Redis())
database = db.getDb("db.json")
databaseD = db.getDb("details.json")
driver = webdriver.Chrome()
scheduler = BackgroundScheduler()

def get_articles(list_name, type_name):
    database = db.getDb("db.json")
    for s in list_name:
        driver.get(s)
        articlesTags = ['h1', 'h2', 'h3', 'h4', 'a']
        linkChecker = ''
        titleChecker = ''
        counter = 0
        c = 0
        for t in articlesTags:
            articles = driver.find_elements_by_tag_name(t)
            for a in articles:        
                try:
                    title = str(a.text)
                    if title != '' and len(title) > 50 and counter < 5:
                        links = driver.find_elements_by_tag_name("a")
                        for l in links:
                            linkUrl = str(l.get_attribute('href'))
                            data = database.getAll()
                            if len(linkUrl) > 50 and SequenceMatcher(None, title, linkUrl).ratio() > 0.3 and counter < 5:
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
                                if counter < 5 and c == 0:
                                    database.add(item)
                                    counter += 1
                                else:
                                    c = 0
                                    break
                except:
                    break


def get_article_details(type_name):
    databaseDet = db.getDb("details.json")
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


def check_for_updates():
    databaseDet = db.getDb("details.json")
    infoTags = ['article', 'div', 'p', 'a', 'span']
    data = databaseDet.getAll()
    for d in range(len(data)):
        counter = 0
        url = data[d]['url']
        infoChecker = data[d]['info']
        driver.get(url)
        for t in infoTags:
            try:
                elements = driver.find_elements_by_tag_name(t)
                for e in elements:
                    for check in range(len(data)):
                        if counter < 1 and len(e.text) > 500 and infoChecker != str(e.text)[0:1000]:
                            dataId = data[d]['id']
                            databaseD.updateById(dataId,{"info":str(e.text)[0:1000]})
                            counter += 1
                        else:
                            break
            except:
                break

def queue_tasks():
#     sport_articles = q.enqueue(get_articles(sport_sites_list, 'sport'))
#     sport_articles_det = q.enqueue(get_articles_details('sport'))
#     business_articles = q.enqueue(get_articles(business_sites_list, 'biznes'))
#     business_articles_det = q.enqueue(get_articles_details('biznes'))
#     moto_articles = q.enqueue(get_articles(moto_sites_list, 'moto'))
#     moto_articles_det = q.enqueue(get_articles_details('moto'))
    get_articles(sport_sites_list, 'sport')
    get_article_details('sport')
    get_articles(moto_sites_list, 'moto')
    get_article_details('moto')
    get_articles(business_sites_list, 'biznes')
    get_article_details('biznes')
    check_for_updates()

# while(True):
    # scheduler.add_job(func=queue_tasks, trigger="interval", minutes=10)
    # q.enqueue_at(timedelta(minutes=10), queue_tasks())

queue_tasks()

driver.close()
driver.quit()
