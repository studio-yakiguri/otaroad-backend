# 카카오 geocoder module by DongHyeong Lee

from requests import get as http_get
from requests import exceptions

from .util import APIKeyLoader

URL: str = "https://dapi.kakao.com/v2/local/search/address.json"

APIKEY: dict = APIKeyLoader('kakao').load()


def is_valid() -> dict:  # 값이 맞는 지 확인
    return


class Geocoding:
    def __init__(self, address) -> None:
        self.address = address
        self.address_data = {
            'address': None,
            'road_address': None,
            'buildng_name': None,
            'x': None,
            'y': None
        }
        self.__get_address_info()

    def __get_address_info(self) -> None:

        # Prepare for request
        api_key = APIKEY['api_key']
        headers: dict = {
            'Authorization': f'KakaoAK {api_key}'
        }
        params: dict = {
            'query': self.address,
            'analyze_type': 'exact'
        }

        # Request from KakaoMap local API
        try:
            resp = http_get(
                url=URL,
                params=params,
                headers=headers
            )
        except exceptions.ConnectionError as con_e:
            print(con_e)
            return
        except exceptions.HTTPError as http_e:
            print(http_e)
            return

        # Data extract from Response
        data: dict = resp.json()
        documents: list = data.get('documents')

        # if documents is empty
        if len(documents) == 0:
            raise ValueError(f"No Data about '{self.address}'")

        address: dict = documents[0]['address']
        road_address: dict = documents[0]['road_address']

        # Data add to self.data
        self.address_data['address'] = address['address_name']
        self.address_data['road_address'] = road_address['address_name']
        self.address_data['buildng_name'] = road_address['building_name']
        self.address_data['x'] = address['x']
        self.address_data['y'] = address['y']

    def data(self) -> dict:
        return self.address_data

    def cordinates(self) -> tuple:
        return (self.address_data['x'], self.address_data['y'])

    def x(self) -> str:
        return self.address_data['x']

    def y(self) -> str:
        return self.address_data['y']
