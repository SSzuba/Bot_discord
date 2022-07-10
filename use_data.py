from pysondb import db
import re 
from datetime import datetime 

database = db.getDb("db.json")


def get_newest_article():
    data = database.getByQuery({"type": "sport"})
    reg = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    temp = 0 
    for d in range(len(data)):
        time = data[d]["timeAdd"]
        time = re.search(reg, str(time))
        time = str(datetime.strptime(time.group(), '%H:%M').time())
        timeAsNumber = time.replace(":","")
        if int(timeAsNumber) > temp:
            temp = timeAsNumber
            return data[d]["title"] + " " + data[d]["url"]
        else: 
            continue
        

def get_articles():
    data = database.getBy({"type": "wiadomości sportowe z piłki nożnej"})
    for i in range(5):
        title = (i, data[i]["title"])
        url = (i, data[i]["url"])
        return title + " " + url
print(get_newest_article())
