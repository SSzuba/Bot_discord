import sqlite3
from datetime import datetime

con = sqlite3.connect("database.db")
cur = con.cursor()
now = datetime.now()
date = now.strftime("%d/%m/%Y %H:%M:%S")

#default data
dataArt = [("Tomaszewski Grzegorza Krychowiaka! Takich słów nikt się nie spodziewał",
            "https://sport.wprost.pl/pilka-nozna/reprezentacja-polski/11077768/jan-tomaszewski-broni-grzegorza-krychowiaka-takich-slow-nikt-sie-nie-spodziewal.html", "det", "sport", date, "New")]

dataSites = [
    ("https://sport.onet.pl", "sport"),
    ("https://sport.wp.pl", "sport"),
    ("https://sport.interia.pl", "sport"),
    ("https://polsatsport.pl", "sport"),
    ("https://gol24.pl", "sport"),
    ("https://eurosport.tvn24.pl", "sport"),
    ("https://sport.fakt.pl", "sport"),
    ("https://sport.wprost.pl", "sport"),
    ("https://biznes.onet.pl", "biznes"),
    ("https://biznes.wp.pl", "biznes"),
    ("https://biznes.interia.pl", "biznes"),
    ("https://pb.pl", "biznes"),
    ("https://money.pl", "biznes"),
    ("https://biznes.wprost.pl", "biznes"),
    ("https://businessinsider.com.pl", "biznes"),
    ("https://moto.onet.pl", "moto"),
    ("https://moto.wp.pl", "moto"),
    ("https://moto.interia.pl", "moto"),
    ("https://auto-swiat.pl", "moto"),
    ("https://moto.pl", "moto"),
    ("https://motofakty.pl", "moto"),
    ("https://auto.wprost.pl", "moto"),
]

def clear_db():
  cur.execute("DROP TABLE articles")
  cur.execute("DROP TABLE sites")

def make_tables():
  cur.execute(
      "CREATE TABLE articles(title TEXT, url TEXT, details TEXT, type TEXT, date TEXT, status TEXT)")
  cur.executemany("INSERT INTO articles VALUES(?, ?, ?, ?, ?, ?)", dataArt)
  con.commit()

  cur.execute(
      "CREATE TABLE sites(url TEXT, type TEXT)")
  cur.executemany("INSERT INTO sites VALUES(?, ?)", dataSites)
  con.commit()

clear_db()
make_tables()

con.close()
