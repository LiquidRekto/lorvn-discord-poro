import requests
import json
response = json.loads(requests.get("your_url").text)

def retrieveCardsData():
    for card in response:
        print(card["cardCode"])
