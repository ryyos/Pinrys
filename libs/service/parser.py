import requests
from urllib.parse import urlencode
from requests import Response
from fake_useragent import FakeUserAgent
from datetime import datetime
from time import time, sleep
from icecream import ic
from typing import Union, List, Dict, Any
from json import dumps

from libs.helpers.Writer import Writer
from libs.utils.ApiRetry import ApiRetry
class Parser:
    def __init__(self) -> None:
        self.__writer = Writer()
        self.__user_agent = FakeUserAgent()
        self.__retry = ApiRetry()
        self.__api = 'https://id.pinterest.com/resource/BaseSearchResource/get/'

        self.__headers = {
            "User-Agent": self.__user_agent.random
        }


    def __create_param(self, query: str, size: int) -> dict:
        return {
            "options": {
                "article": "",
                "appliedProductFilters": "---",
                "price_max": "null",
                "price_min": "null",
                "scope": "pins",
                "auto_correction_disabled": "",
                "top_pin_id": "",
                "filters": "",
                "query": query,
                "page_size": size
            }
        }


    def execute_query(self, name: str) -> dict:

        response: Response = self.__retry.get(url=f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&data={str(self.__create_param(query=name))}', headers=self.__headers)
        resource: dict = response.json()["resource_response"]
        
        # results = {
        #     "status": resource["status"],
        #     "message": resource["message"],
        #     "total": len(resource["data"]["results"]),
        #     "data": [
        #         {
        #             "description": data["description"],
        #             "author": {
        #                 "name": data["pinner"]["full_name"],
        #                 "username": data["pinner"]["username"],
        #                 "followers": data["pinner"]["follower_count"]
        #             },
        #             "created": data["created_at"],
        #             "title": data["title"],
        #             "content_domain": data["domain"],
        #             "images": data["images"]
        #         } for data in resource["data"]["results"]
        #     ]
        # }

        # self.__writer.write_json(path=f'data/results.json', content=results)


    def main(self, name: str):

        url = f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&{str(self.__payload)}'

        response = requests.get(url=url, headers=self.__headers)
        ic(response)

        results = {
            "domain": self.__api.split("/")[2],
            "crawling_time": datetime.now(),
            "crawling_time_epoch": int(time()),
            "query": name,
            "url": url,

        }


        # self.__writer.ex(path=f'data/{name.replace(" ", "_")}.json', content=response.json())
        bookmark = response.json()["resource_response"]["bookmark"]


if __name__ == '__main__':
    main = Parser()
    main.extract_data('freya')


"""
"""