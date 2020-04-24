import requests
import json
response = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)

def retrieveCardsData():
    for card in response:
        print(card["cardCode"])
