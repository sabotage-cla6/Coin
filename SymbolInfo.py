import requests
import json
from pymongo import MongoClient


class SymbolInfo:
    ENDPOINT: str = 'https://api.coin.z.com/public'
    TICKER_PATH: str = '/v1/ticker?symbol={}'

    DB_SERVER: str = 'mongodb://localhost:27017/'
    DB_NAME: str = 'COIN'

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.mongo_client = MongoClient(SymbolInfo.DB_SERVER)
        self.db = self.mongo_client.COIN

    def get_ticker(self):
        path = SymbolInfo.TICKER_PATH.format(self.symbol)

        response = requests.get(SymbolInfo.ENDPOINT + path)
        print(json.dumps(response.json(), indent=2))

#        resdata: json = json.dumps(response.json(), indent=2)
        self.db.Ticker.insert_one(response.json())


symbol1 = SymbolInfo('XRP_JPY')
symbol1.get_ticker()
