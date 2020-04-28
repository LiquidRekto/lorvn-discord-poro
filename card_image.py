import requests
import json

response1 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)
response2 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/en_us/data/set2-en_us.json").text)

image_urls = {}

for card in response1:
    image_urls[card['name']] = { "CardArt": f"{(card['assets'])['gameAbsolutePath']}", "FullArt": f"{(card['assets'])['fullAbsolutePath']}" }

for card in response2:
   image_urls[card['name']] = { "CardArt": f"{(card['assets'])['gameAbsolutePath']}", "FullArt": f"{(card['assets'])['fullAbsolutePath']}" }