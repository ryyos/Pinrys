import requests
from libs.helpers.Writer import Writer
from fake_useragent import FakeUserAgent
from icecream import ic
class Parser:
    def __init__(self) -> None:
        self.__writer = Writer()
        self.__user_agent = FakeUserAgent()
        self.__api = 'https://id.pinterest.com/resource/BaseSearchResource/get/'

        self.__headers = {
            "User-Agent": self.__user_agent.random
        }
        pass

    def extract_data(self, name: str):
        data = {
            "options": {
                "article": "",
                "appliedProductFilters": "---",
                "price_max": "null",
                "price_min": "null",
                "query": name,
                "scope": "pins",
                "auto_correction_disabled": "",
                "top_pin_id": "",
                "filters": ""
            }
        }
        
        response = requests.get(url=f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&{str(data)}', headers=self.__headers)
        print(f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&{str(data)}')
        ic(response)
        self.__writer.ex(path=f'data/{name.replace(" ", "_")}.json', content=response.json())

if __name__ == '__main__':
    main = Parser()
    main.extract_data('freya')