from pysondb import db
import re 
from datetime import datetime 

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
        

def get_articles():
    data = database.getBy({"type": 'sport'})
    for i in range(len(data)):
        title = (i, data[i]["title"])
        url = (i, data[i]["url"])
        return title + " " + url

