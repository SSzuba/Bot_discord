# Bot_discord

Do uruchomienia programu służy plik main.py

Bot wykorzystuje bibliotekę Selenium, w tym celu potrzebujemy obsługę sterownika, która jest zdefiniowana w pliku get_data.py

Możemy wykorzystać lokalny sterownik znajdujący się w folderze projektu, w tym celu należy pobrać odpowiednią wersję chromedriver kompatybilną z używaną wersją chrome (w projekcie zawarty chromedriver w wersji 108.0.5359.71) lub wykorzystać środowisko docker z wykorzystaniem komendy "docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome"

Aby wybrać sposób obsługi sterownika, należy odkomentować i zakomentować odpowienie linie w pliku get_data.py. 

Dla sterownika lokalnego:
- zakomentować linię nr 13 i odkomentować linię nr 11

Dla sterownika docker:
- zakomentować linię nr 11 i odkomentować linię nr 13

