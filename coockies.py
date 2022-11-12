import re

reTypes = ["^Akcept", "^Prze", "^Zgadzam", "^Wyr", "^Zaakceptuj"]

def coockies_accept(buttons):

    for b in buttons:
        for t in reTypes:
            if re.search(str(b.text),t): 
                return b.text
                break
            # elif re.search(str(b.text).upper,t): 
            #     b.click()
            #     break
            # elif re.search(str(b.text).lower,t): 
            #     b.click()
            #     break
