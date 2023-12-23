import requests
from requests import Response
from typing import Union
from time import sleep
from icecream import ic


class ApiRetry:
    def __init__(self) -> None:
        pass

    def get(self, url: str, headers: dict, max_retries: int = 5, retry_interval: Union[int, float] = 0.2):
        for _ in range(max_retries):
            try:
                response = requests.get(url=url, headers=headers)
                ic(response)
                return response
            except Exception as err:
                # self.__logs.err(message=err, url=url)
                ic(err)
            sleep(retry_interval)
            retry_interval+= 0.2
        

    def post(self, url: str, headers: dict, max_retries: int = 5, retry_interval: Union[int, float] = 0.2, payload: any = None):
        for _ in range(max_retries):
            try:
                response = requests.post(url=url, headers=headers, data=payload)
                ic(response)
                return response
            except Exception as err:
                # self.__logs.err(message=err, url=url)
                ic(err)
            sleep(retry_interval)
            retry_interval+= 0.2
        
