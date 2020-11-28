import requests
import json
response1 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/vi_vn/data/set1-vi_vn.json").text)
response2 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/vi_vn/data/set2-vi_vn.json").text)
try:
    response3 = json.loads(requests.get("http://dd.b.pvp.net/latest/set3/vi_vn/data/set3-vi_vn.json").text)
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



