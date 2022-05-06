from pysondb import db

database = db.getDb("db.json")
titles = []
urls = []


def get_articles():
    data = database.getBy({"type": "wiadomości sportowe z piłki nożnej"})
    for i in range(5):
        titles.insert(i, data[i]["title"])
        urls.insert(i, data[i]["url"])
        print(titles[i] + " " + urls[i])
