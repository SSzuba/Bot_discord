import re 

reg = '([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
time = re.search(reg, "dzisiaj 21:32") 
print(time)      
