import requests
import json

response1 = json.loads(requests.get("http://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json").text)
response2 = json.loads(requests.get("http://dd.b.pvp.net/latest/set2/en_us/data/set2-en_us.json").text)

image_urls = {}

for card in response1:
    source = (card['assets'])[0]
    image_urls[card['name']] = { "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" }

for card in response2:
   source = (card['assets'])[0]
   image_urls[card['name']] = { "CardArt": f"{source['gameAbsolutePath']}", "FullArt": f"{source['fullAbsolutePath']}" }