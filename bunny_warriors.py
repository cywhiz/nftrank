import requests
import json
from bs4 import BeautifulSoup

url = 'https://moonrank.app/mints/bunny_warriors'
resp = requests.get(url).json()

data = {}
data['items'] = []

for row in resp['mints']:
    data['items'].append({
        'rank': row['rank'],
        'id': row['name'],
        'image': row['image'],
        'link': 'https://moonrank.app/collection/bunny_warriors/' + row['mint']
    })

with open('bunny.json', 'w') as f:
    json.dump(data, f)