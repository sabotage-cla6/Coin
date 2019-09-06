import requests
import json


class CoinInfo:
    ENDPOINT: str = 'https://api.coin.z.com/public'
    TICKERPATH:str = '/v1/ticker?symbol={}'

    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_ticker(self):
        path = CoinInfo.TICKERPATH.format(self.symbol)

        response = requests.get(CoinInfo.ENDPOINT + path)
        print(json.dumps(response.json(), indent=2))


symbol1 = CoinInfo('XRP_JPY')
symbol1.get_ticker()
