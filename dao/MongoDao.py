from datetime import datetime, timedelta, timezone
import pymongo
from pymongo import MongoClient
import json
import pytz


class MongoDao:
    DB_SERVER: str = 'mongodb://localhost:27017/'
    DB_NAME: str = 'COIN'

    MONGO_CLIENT = MongoClient(DB_SERVER)
    DB = MONGO_CLIENT.COIN

    @staticmethod
    def insert_one(symbol_name: str, json_data: json):
        MongoDao.DB[symbol_name].insert_one(json_data['data'][0])

    @staticmethod
    def find(symbol_name: str):
        row_idx: int = 0
        for data in MongoDao.DB[symbol_name].find() \
                .sort('timestamp', pymongo.DESCENDING):
            row_idx = row_idx + 1
            print(data)
            if row_idx >= 100:
                break

    def find_high(symbol_name: str) -> dict:
        result: dict = {}

        row_idx: int = 0
        for data in MongoDao.DB[symbol_name].find() \
                .sort('timestamp', pymongo.DESCENDING):
            row_idx = row_idx + 1
            time: datetime = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
            time = time.astimezone(timezone(timedelta(hours=+9)))
            result[datetime.strftime(time, "%Y/%m/%d %H:%m:%s")] = data["high"]
            if row_idx >= 100:
                break
        return result


aaa = MongoDao.find_high("XRP_JPY")
print(aaa.get(0))
