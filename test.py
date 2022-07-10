import re 
from datetime import datetime

reg = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
time = re.search(reg, "dzisiaj 21:32") 
time = datetime.strptime(time.group(), '%H:%M').time()
time = str(time)
print(time.replace(":",""))
