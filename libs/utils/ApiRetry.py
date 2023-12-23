from typing import Union
from time import sleep

class ApiRetry:
    def __init__(self, url: str, headers: dict, max_retries: int = 5, retry_interval: Union[int, float] = 0.2):
        self.url = url
        self.headers = headers
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    def get(self):
        # Implementasi logika retry untuk HTTP GET
        pass

    def post(self):
        # Implementasi logika retry untuk HTTP POST
        pass
