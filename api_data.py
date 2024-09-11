import requests
from config import api
from typing import Any, Dict, Union


def get_json(pair: str) -> Dict[str, Any]:
    # getting json from binance api
    url = "https://binance43.p.rapidapi.com/ticker/24hr"

    querystring = {"symbol": pair}

    headers = {
        "x-rapidapi-key": api,
        "x-rapidapi-host": "binance43.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    return response.json()


def get_lowprice(pair: str) -> Union[str, Dict[str, Any]]:
    # getting lowprcie from json
    data = get_json(pair)
    if 'lowPrice' in data:
        return data['lowPrice']
    else:
        return data


def get_highprice(pair: str) -> Union[str, Dict[str, Any]]:
    # getting highprice from json
    data = get_json(pair)
    if 'highPrice' in data:
        return data['highPrice']
    else:
        return data


def get_lastprice(pair: str) -> Union[str, Dict[str, Any]]:
    # getting lastprice from json
    data = get_json(pair)
    if 'lastPrice' in data:
        return data['lastPrice']
    else:
        return data


def get_price_change(pair: str) -> Union[str, Dict[str, Any]]:
    # getting price change from json
    data = get_json(pair)
    if 'priceChange' in data:
        return data['priceChange']
    else:
        return data


def get_price_change_percent(pair: str) -> Union[str, Dict[str, Any]]:
    # getting price change in percent from json
    data = get_json(pair)
    if 'priceChangePercent' in data:
        return data['priceChangePercent'] + '%'
    else:
        return data
