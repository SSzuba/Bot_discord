from pysondb import db
import re
from datetime import datetime
from difflib import SequenceMatcher
import pandas as pd
from fuzzywuzzy import fuzz

database = db.getDb("details.json")


def get_articles(type):
        data = database.getByQuery({"type": str(type)})
        title = data[len(data)-1]["title"]
        url = data[len(data)-1]["url"]
        return title + " " + url


def get_articles_by_title(title):
    data = database.getAll()
    for i in range(len(data)):
        dataTitle = data[i]['title']
        url = data[i]['url']
        # dodać sprawdzenie

        # if dataTitle.find(str(title)) > 10:
        if SequenceMatcher(None, str(dataTitle), str(title)).ratio() > 0.3:
            # print(fuzz.ratio(title, dataTitle))
            # if fuzz.ratio(title, dataTitle) >= 30:
            return dataTitle + ' ' + url
            # print(msg)
        else:
            msg = 'Brak artykułów'
    return msg

# print(get_articles_by_title('leo messi nie trenuje'))
