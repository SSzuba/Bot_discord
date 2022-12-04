sites = [
    'onet.pl',
    'wp.pl',
    'interia.pl',
    'tvp.pl',
    'tvn24.pl',
    'fakt.pl',
    'wprost.pl'
]

sport_sites = [
    'meczyki.pl',
    'polsatsport.pl',
    'gol24.pl'
]

buisness_sites = [
    'businessinsider.com.pl',
    'pb.pl',
    'money.pl'
]

moto_sites = [
    'auto-swiat.pl',
    'moto.pl',
    'motofakty.pl'
]

sport_sites_list = []
moto_sites_list = []
buisness_sites_list = []

for s in sites:
    sport_sites.append('sport.'+s)
    buisness_sites.append('biznes.'+s)
    moto_sites.append('motoryzacja.'+s)

for s in sport_sites:
    sport_sites_list.append("https://" + s)
for s in buisness_sites:
    moto_sites_list.append("https://" + s)
for s in moto_sites:
    buisness_sites_list.append("https://" + s)
