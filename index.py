import requests, json, cloudscraper
from flask import Flask, render_template, request

app = Flask(__name__)

def get_key(id, key):
    collection = request.form['collection'].replace('-', '_')

    with open(collection + '.json', 'r') as f:
        data = json.loads(f.read())
        item = data['items']

    d = [x for x in item if x["id"] == id]

    return d[0][key]

def get_alpha():
    collection = request.form['collection'].replace('_', '-')
    limit = request.form.get('limit', type=int)

    url = "https://apis.alpha.art/api/v1/collection"
    params = '{"collectionId":"' + collection + '","orderBy":"PRICE_LOW_TO_HIGH","status":["BUY_NOW"],"traits":[]}'
    resp = requests.post(url, data=params)
    items = resp.json()['tokens']
    items = items[0:limit]

    for item in items:
        item['price'] = int(item['price']) / 1000000000
        item['details'] = get_key(item['title'], 'link')
        item['rank'] = get_key(item['title'], 'rank')
        item['buy'] = 'https://alpha.art/t/' + item.pop('mintId')

    return items

def get_magic():
    collection = request.form['collection'].replace('_', '-')
    limit = request.form['limit']
    url = "https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22" + collection + "%22%7D%2C%22%24sort%22%3A%7B%22takerAmount%22%3A1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A" + limit + "%2C%22status%22%3A%5B%5D%7D"

    # lowest
    # https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22shrooms%22%7D%2C%22%24sort%22%3A%7B%22takerAmount%22%3A1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A20%2C%22status%22%3A%5B%5D%7D

    # recent
    # https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22shrooms%22%7D%2C%22%24sort%22%3A%7B%22createdAt%22%3A-1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A20%2C%22status%22%3A%5B%5D%7D

    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    items = resp.json()['results']

    for item in items:
        item['image'] = item.pop('img')
        item['details'] = get_key(item['title'], 'link')
        item['rank'] = get_key(item['title'], 'rank')
        item['buy'] = 'https://magiceden.io/item-details/' + item.pop('mintAddress')

    return items   

# ========== HOMEPAGE ==========
@app.route("/")
def index():
    return render_template("index.html")

# ========== RESULTS PAGE ==========
@app.route("/results", methods=["GET", "POST"])
def results():
    # Redirect to index page if results page is accessed directly
    if request.method == "GET":
        return index()

    # Get data from user inputs in form fields
    if (request.form['site'] == 'magic'):
        items = get_magic()
    else:
        items = get_alpha()

    return render_template("results.html", items=items)

if __name__ == "__main__":
    app.run()