import requests
import json
response1 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/vi_vn/data/set1-vi_vn.json").text)
response2 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/vi_vn/data/set2-vi_vn.json").text)
response3 = json.loads(requests.get("http://dd.b.pvp.net/latest/set3/vi_vn/data/set3-vi_vn.json").text)
response4 = json.loads(requests.get("http://dd.b.pvp.net/latest/set4/vi_vn/data/set4-vi_vn.json").text)
try:
    response5 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)
    response6 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/en_us/data/set2-en_us.json").text)
    response7 = json.loads(requests.get("http://dd.b.pvp.net/latest/set3/en_us/data/set3-en_us.json").text)
    response8 = json.loads(requests.get("http://dd.b.pvp.net/latest/set4/en_us/data/set4-en_us.json").text)
except Exception as e:
    print(e)

cards_data = {}

for card in response1:
    cards_data[card['cardCode']] = { "Name": f"{card['name']}"}

for card in response2:
   cards_data[card['cardCode']] = { "Name": f"{card['name']}"}

for card in response3:
   cards_data[card['cardCode']] = { "Name": f"{card['name']}"}
                                   
for card in response4:
   cards_data[card['cardCode']] = { "Name": f"{card['name']}"}

try:
    for card in response5:
        cards_data[card['cardCode']] = { "Name": f"{card['name']}"}
                                        
    for card in response6:
        cards_data[card['cardCode']] = { "Name": f"{card['name']}"}
                                        
    for card in response7:
        cards_data[card['cardCode']] = { "Name": f"{card['name']}"}
                                        
    for card in response8:
        cards_data[card['cardCode']] = { "Name": f"{card['name']}"}
except Exception as e:
    print(e)



