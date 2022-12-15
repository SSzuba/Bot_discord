sites = [
    'onet.pl',
    'wp.pl',
    'interia.pl',
]

sport_sites = [
    'meczyki.pl',
    'polsatsport.pl',
    'gol24.pl',
    'eurosport.tvn24.pl',
    'sport.fakt.pl',
    'sport.wprost.pl'
]

business_sites = [
    'businessinsider.com.pl',
    'pb.pl',
    'money.pl',
    'biznes.wprost.pl'
]

moto_sites = [
    'auto-swiat.pl',
    'moto.pl',
    'motofakty.pl',
    'auto.wprost.pl'
]

sport_sites_list = []
moto_sites_list = []
business_sites_list = []

for s in sites:
    sport_sites.append('sport.'+s)
    business_sites.append('biznes.'+s)
    moto_sites.append('motoryzacja.'+s)

for s in sport_sites:
    sport_sites_list.append("https://" + s)
for s in moto_sites:
    moto_sites_list.append("https://" + s)
for s in business_sites:
    business_sites_list.append("https://" + s)
