from pysondb import db
import re 
from datetime import datetime 
from difflib import SequenceMatcher

database = db.getDb("details.json")


def get_newest_article():
    data = database.getByQuery({"type": "sport"})
    reg = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    temp = 0 
    for d in range(len(data)):
        time = data[d]["time"]
        time = re.search(reg, str(time))
        time = str(datetime.strptime(time.group(), '%H:%M').time())
        timeAsNumber = int(time.replace(":",""))
        if temp < timeAsNumber:
            temp = timeAsNumber
            msg = data[d]["title"] + " " + data[d]["url"]
        
    return msg
        

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
        if dataTitle.find(str(title)):
        # if SequenceMatcher(None, str(dataTitle), str(title)).ratio() > 0.2:
            return dataTitle + ' ' + url
        else:
            return 'Brak artykułów' 

print(get_articles_by_title('Polska'))
