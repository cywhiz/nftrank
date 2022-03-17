import requests
import json
from bs4 import BeautifulSoup

collection = 'bunny_warriors'
url = 'https://moonrank.app/mints/' + collection
items = requests.get(url).json()

data = {}
data['items'] = []

for item in items['mints']:
    data['items'].append({
        'rank': item['rank'],
        'id': item['name'],
        'image': item['image'],
        'link': 'https://moonrank.app/collection/' + collection + '/' + item['mint']
    })

with open(collection + '.json', 'w') as f:
    json.dump(data, f)