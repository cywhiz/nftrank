import requests, json
import cloudscraper

# def get_alpha():
#     collection = 'shrooms'
#     limit = 10

#     url = "https://apis.alpha.art/api/v1/collection"
#     params = '{"collectionId":"' + collection + '","orderBy":"PRICE_LOW_TO_HIGH","status":["BUY_NOW"],"traits":[]}'
#     resp = requests.post(url, data=params)
#     items = resp.json()['tokens']
#     items = items[0:limit]

#     return items

def get_alpha():
    collection = 'shrooms'
    limit = '10'

    scraper = cloudscraper.create_scraper()
    url = "https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q=%7B%22%24match%22%3A%7B%22collectionSymbol%22%3A%22shrooms%22%7D%2C%22%24sort%22%3A%7B%22takerAmount%22%3A1%7D%2C%22%24skip%22%3A0%2C%22%24limit%22%3A20%2C%22status%22%3A%5B%5D%7D"

    resp = scraper.get(url)
    # items = resp.json()

    return resp.text

print(get_alpha())