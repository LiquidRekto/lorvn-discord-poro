import requests
import json
response1 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)
response2 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/en_us/data/set2-en_us.json").text)
try:
    response3 = json.loads(requests.get("http://dd.b.pvp.net/latest/set3/en_us/data/set3-en_us.json").text)
except Exception as e:
    print(e)

cards_data = {}

for card in response1:
    cards_data[card['cardCode']] = { "Name": f"{card['name']}"}

for card in response2:
   cards_data[card['cardCode']] = { "Name": f"{card['name']}"}

try:
    for card in response3:
        cards_data[card['cardCode']] = { "Name": f"{card['name']}"}
except Exception as e:
    print(e)



