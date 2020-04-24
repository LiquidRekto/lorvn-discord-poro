import requests

r = requests.get('http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json')
data = r.json()

def retrieveCardsData():
    for card in data:
        print(data["cardCode"])
