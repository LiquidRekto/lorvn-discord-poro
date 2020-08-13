import requests
import json

response1 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)
response2 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/en_us/data/set2-en_us.json").text)
try:
    response3 = json.loads(requests.get("http://dd.b.pvp.net/latest/set3/en_us/data/set3-en_us.json").text)
except Exception as e:
    print(e)

image_urls = {}

for card in response1:
    image_urls.setdefault(card['name'], [])
    source = (card['assets'])[0]      
    if card['levelupDescription'] == "" and card['rarity'] == "None":
        image_urls[card['name']].append({"isLevelledUp": True, "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
    elif card['levelupDescription'] != "" and card['rarity'] == "Champion":
        image_urls[card['name']].append({"isLevelledUp": False, "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
    elif card['rarity'] != "Champion":
        image_urls[card['name']].append({ "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })

for card in response2:
    image_urls.setdefault(card['name'], [])
    source = (card['assets'])[0]      
    if card['levelupDescription'] == "" and card['rarity'] == "None":
        image_urls[card['name']].append({"isLevelledUp": True, "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
    elif card['levelupDescription'] != "" and card['rarity'] == "Champion":
        image_urls[card['name']].append({"isLevelledUp": False, "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
    else:
        image_urls[card['name']].append({ "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
                                         
try:
    for card in response3:
    image_urls.setdefault(card['name'], [])
    source = (card['assets'])[0]      
    if card['levelupDescription'] == "" and card['rarity'] == "None":
        image_urls[card['name']].append({"isLevelledUp": True, "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
    elif card['levelupDescription'] != "" and card['rarity'] == "Champion":
        image_urls[card['name']].append({"isLevelledUp": False, "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
    else:
        image_urls[card['name']].append({ "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" })
except Exception as e:
    print(e)
    
    
