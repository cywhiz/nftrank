import requests
import json
from bs4 import BeautifulSoup

url = 'https://shroomstopia.io/rarity'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
nft = soup.find_all('div', class_='nft')

data = {}
data['items'] = []

for row in nft:
    data['items'].append({
        'rank': row.p.text.replace('Ranked #', ''),
        'id': row.h6.text,
        'image': row.find('img')['data-src'],
        'link': url + row.find('a')['href']
    })

with open('shrooms.json', 'w') as f:
    json.dump(data, f)