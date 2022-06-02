
accept_list = [
    "Zgadzam się",
    "Akceptuję",
    "Akceptuj wszystko",
    "Akceptuję i przechodzę do serwisu",
    "Przejdź do serwisu",
    "Zaakceptuj wszystko"
]

def coockies_accept(buttons):

    for b in buttons:
        if str(b.text) == "Zgadzam się".upper(): 
            b.click()
            break
        elif str(b.text) == "Akceptuję".upper():
            b.click()
            break
        elif str(b.text) == "Akceptuj wszystko".upper(): 
            b.click()
            break
        elif str(b.text) == "Akceptuję i przechodzę do serwisu".upper(): 
            b.click()
            break
        elif str(b.text) == "Przejdź do serwisu".upper(): 
            b.click()
            break
        elif str(b.text) == "Zaakceptuj wszystko".upper(): 
            b.click()
            break
        elif str(b.text) == "Zgadzam się": 
            b.click()
            break
        elif str(b.text) == "Akceptuję": 
            b.click()
            break
        elif str(b.text) == "Akceptuj wszystko": 
            b.click()
            break
        elif str(b.text) == "Akceptuję i przechodzę do serwisu": 
            b.click()
            break
        elif str(b.text) == "Przejdź do serwisu": 
            b.click()
            break
        elif str(b.text) == "Zaakceptuj wszystko": 
            b.click()
            break
