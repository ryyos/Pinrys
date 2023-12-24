import requests
import os

import urllib.request
from urllib.parse import urlencode
from requests import Response
from fake_useragent import FakeUserAgent
from datetime import datetime
from time import time, sleep
from icecream import ic
from json import dumps

from libs.utils.Logs import logger
from libs.helpers.Writer import Writer
from libs.utils.ApiRetry import ApiRetry
class Pinterest:
    def __init__(self) -> None:
        self.__writer = Writer()
        self.__user_agent = FakeUserAgent()
        self.__retry = ApiRetry()
        self.__api = 'https://id.pinterest.com/resource/BaseSearchResource/get/'
        self.__base_url = "https://id.pinterest.com"

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


    def __downloader(self, url: str, path: str):
        urllib.request.urlretrieve(url, path)



    def __extract_data(self, resource: dict, query: str) -> dict:
        return {
            "domain": self.__api.split("/")[2],
            "crawling_time": datetime.now(),
            "crawling_time_epoch": int(time()),
            "query": query,
            "content": {
                "status": resource["status"],
                "message": resource["message"],
                "total": len(resource["data"]["results"]),
                "data": [
                    {
                        "url": f'{self.__base_url}/pin/{data["id"]}',
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
        }


    def __search(self, name: str, size: int) -> dict:
        
        response: Response = self.__retry.get(
                url=f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&data={dumps(self.__create_param(query=name, size=size))}', \
                headers=self.__headers
            )
        
        resource: dict = response.json()["resource_response"]
        if not len(resource["data"]["results"]): return False

        logger.info(f"{name} query was found")
        logger.info(f'status {response.status_code}')
        logger.info(f"data extracted successfully")

        return self.__extract_data(resource=resource, query=name)


    def main(self, name: str, size: int):

        results = self.__search(name=name, size=size)
        if not results: return True

        if not os.path.exists(path=f"data/{name.replace(' ', '_')}"):

            os.mkdir(path=f"data/{name.replace(' ', '_')}")
            logger.info(f"create folder data/{name.replace(' ', '_')}")

            os.mkdir(path=f"data/{name.replace(' ', '_')}/image")
            logger.info(f"create folder data/{name.replace(' ', '_')}/image")

            os.mkdir(path=f"data/{name.replace(' ', '_')}/json")
            logger.info(f"create folder data/{name.replace(' ', '_')}/json")

        for ind, url in enumerate(results["content"]["data"]):
            logger.info(f"{name}_{ind} is being downloaded")

            self.__downloader(url=url["images"]["orig"]["url"], path=f"data/{name.replace(' ', '_')}/image/{name.replace(' ', '_')}_{ind}.jpg")
            logger.info(f"{name}_{ind} downloaded successfully")

        self.__writer.write_json(path=f"data/{name.replace(' ', '_')}/json/{name.replace(' ', '_')}.json", content=results)
