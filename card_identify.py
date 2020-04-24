import requests
import json
response = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)

cards_data = {}

for card in response:
    cards_data[card['cardCode']] = { "Name": f"{card['name']}"}



    
