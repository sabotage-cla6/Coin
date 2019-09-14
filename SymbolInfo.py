from datetime import datetime
from datetime import time
from datetime import timedelta
import requests
from bson import json_util

import pymongo
from enum import Enum
import re
import time


class SymbolInfo:
    _DB_SERVER: str = 'mongodb://localhost:27017/'
    _DB_NAME: str = 'COIN'

    _MONGO_CLIENT = pymongo.MongoClient(_DB_SERVER)
    _DB = _MONGO_CLIENT.COIN

    class SYMBOLS(Enum):
        def __init__(self, gmo_name, dmm_name, dmm_req_name, gmo_url_path):
            self.gmo_name = gmo_name
            self.dmm_name = dmm_name
            self.dmm_req_name = dmm_req_name
            self.dmm_url_path = gmo_url_path

        FX_BTC_JPY = ("BTC_JPY", "FX_BTC/JPY", "FX_BTC-JPY", "btc_jpy")
        FX_XRP_JPY = ("XRP_JPY", "FX_XRP/JPY", "FX_XRP-JPY", "xrp_jpy")

    ENDPOINT: str = 'https://api.coin.z.com/public'
    TICKER_PATH: str = '/v1/ticker?symbol={}'

    def __init__(self, symbol: SYMBOLS):
        self.symbol = symbol

    def save_chart(self):
        response = requests.get("https://bitcoin.dmm.com/trade_chart_rate_list/" + self.symbol.dmm_url_path)
        regex = re.compile(('<meta name="csrf-token" content="([^"]*)">'))
        token = regex.search(response.text).group(1)

        param = {"_token": token, "currency_name": self.symbol.dmm_req_name, "foot": "ONE_MIN", "type": "BID"}
        response = requests.post("https://bitcoin.dmm.com/api/get_realtime_chart", param)

        temp_data = response.json()["chart"][self.symbol.dmm_name]["ONE_MIN"]["BID"]

        # prevent insert duplicated data.
        # use tmp collection. and select data need to insert.
        max_date_registed = SymbolInfo._DB[self.symbol.name].find(projection={"d": 1}). \
            sort("d", pymongo.DESCENDING).limit(1)[0]["d"]
        tmp_collection_name: str = "tmp_{0}_{1}".format(self.symbol.name, time.time())
        SymbolInfo._DB[tmp_collection_name].insert_many(temp_data)
        find_temp_data = SymbolInfo._DB[tmp_collection_name].find({"d": {"$gt": max_date_registed}})
        insert_data = [x for x in find_temp_data]
        SymbolInfo._DB[self.symbol.name].insert_many(insert_data)
        SymbolInfo._DB[tmp_collection_name].drop()


if __name__ == '__main__':

    prev_time: datetime = datetime.now()

    while 1 == 1:
        now_time: datetime = datetime.now()
        symbol1 = SymbolInfo(SymbolInfo.SYMBOLS.FX_BTC_JPY)
        symbol1.save_chart()
        symbol1 = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
        symbol1.save_chart()
        prev_time = now_time

        # I will make this program get data per minute.
        # so. i define strictly next time this process run.
        # and, in case machine clock is little off, seconds set 10
        next_planned_time = datetime(now_time.year, now_time.month, now_time.day
                                     , now_time.hour, now_time.minute, 10)
        next_planned_time = next_planned_time + timedelta(hours=1)
        time.sleep((next_planned_time - now_time).total_seconds());
