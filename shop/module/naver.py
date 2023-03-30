# 네이버 geocoder module by DongHyeong Lee

from requests import get as http_get
from requests import exceptions

from .util import APIKeyLoader

URL: str = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

APIKEY: dict = APIKeyLoader('naver').load()


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
        client_id: str = APIKEY['client_id']
        client_secret: str = APIKEY['client_secret']

        headers: dict = {
            'X-NCP-APIGW-API-KEY-ID': client_id,
            'X-NCP-APIGW-API-KEY': client_secret
        }
        params: dict = {
            'query': self.address,
        }

        # Request from NaverOpen API
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
        addresses: list = data.get('addresses')

        # if addresses is empty
        if len(addresses) == 0:
            raise ValueError(f"No Data about '{self.address}'")

        # Data add to self.data
        self.address_data['address'] = addresses[0]['jibunAddress']
        self.address_data['road_address'] = addresses[0]['roadAddress']
        self.address_data['buildng_name'] = self.address_data['address'].split()[-1]
        self.address_data['x'] = addresses[0]['x']
        self.address_data['y'] = addresses[0]['y']

    def data(self) -> dict:
        return self.address_data

    def cordinates(self) -> tuple:
        return (self.address_data['x'], self.address_data['y'])

    def x(self) -> str:
        return self.address_data['x']

    def y(self) -> str:
        return self.address_data['y']
