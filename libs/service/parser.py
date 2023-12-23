import requests

from requests import Response
from fake_useragent import FakeUserAgent
from datetime import datetime
from time import time, sleep
from icecream import ic
from typing import Union, List, Dict, Any

from libs.helpers.Writer import Writer
class Parser:
    def __init__(self) -> None:
        self.__writer = Writer()
        self.__user_agent = FakeUserAgent()
        self.__api = 'https://id.pinterest.com/resource/BaseSearchResource/get/'

        self.__headers = {
            "User-Agent": self.__user_agent.random
        }
        self.__payload = {
            "options": {
                "article": "",
                "appliedProductFilters": "---",
                "price_max": "null",
                "price_min": "null",
                "scope": "pins",
                "auto_correction_disabled": "",
                "top_pin_id": "",
                "filters": ""
            }
        }


    def __retry(self, url: str, max_retries: int= 5, retry_interval: Union[int, float] = 0.2) -> Response :

        def get():
            for _ in range(max_retries):
                try:
                    response = requests.get(url=url, headers=self.__headers)
                    ic(response)
                    return response
                except Exception as err:
                    # self.__logs.err(message=err, url=url)
                    ic(err)
                sleep(retry_interval)
                retry_interval+= 0.2
            return response
        
        def post():
            for _ in range(max_retries):
                try:
                    response = requests.post(url=url, headers=self.__headers)
                    ic(response)
                    return response
                except Exception as err:
                    # self.__logs.err(message=err, url=url)
                    ic(err)
                sleep(retry_interval)
                retry_interval+= 0.2
            return response


    def __next_steps(self, bookmark: str) -> List(Dict["str", Any]):
        pass

    def execute_query(self, name: str) -> dict:
        self.__payload["query"] = name

        response: Response = self.__retry(url=f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&{str(self.__payload)}')
        resource: dict = response.json()["resource_response"]
        
        results = {
            "status": resource["status"],
            "message": resource["message"],
            "total": len(resource["data"]["results"]),
            "data": [
                {
                    "description": data["description"],
                    "author": {
                        "name": data["pinner"]["full_name"],
                        "username": data["pinner"]["username"],
                        "followers": data["pinner"]["follower_count"]
                    },
                    "created": data["created_at"],
                    "title": data["title"],
                    "content_domain": data["domain"],
                    "images": data["images"]
                } for data in resource["data"]["results"]
            ]
        }

        self.__writer.write_json(path=f'data/results.json', content=results)


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
    def next_steps(self, name: str):
        response = requests.post(url=self.__api, headers=self.__headers)


if __name__ == '__main__':
    main = Parser()
    main.extract_data('freya')


"""
"""