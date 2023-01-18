from pysondb import db
from datetime import datetime
from difflib import SequenceMatcher

database = db.getDb("details.json")


def get_articles(type):
        data = database.getByQuery({"type": str(type)})
        title = data[len(data)-1]["title"]
        url = data[len(data)-1]["url"]
        return title + " " + url
