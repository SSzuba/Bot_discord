from pysondb import db

database = db.getDb("db.json")
titles = []
urls = []


def get_articles():
    data = database.getBy({"type": "sport"})
    title = data[0]["title"]
    url = data[0]["url"]
    #print(titles[0] + " " + urls[0])
    msg = title + " " + url
    return msg
