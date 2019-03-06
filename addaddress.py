import requests
from copyheaders import headers_raw_to_dict
from ut import getaccounts

s = requests.Session()

# request headers
ua = b"""
"""

s.headers = headers_raw_to_dict(ua)


def getbnb(accounts):

    url = "https://www.binance.com/gateway-api/v1/private/dex-campaign/add-addresses"
    data = {"addresses": accounts}
    z = s.post(url, json=data)
    print(z.json())


if __name__ == "__main__":
    accounts = getaccounts()
