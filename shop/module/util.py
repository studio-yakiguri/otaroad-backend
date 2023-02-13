import os
import json
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path


def api_server_check(url: str, api_key: dict) -> dict:  # API Server Check
    service: str = ''
    p = re.compile('[a-z]+')
    result: dict = {
        'service': service,
        'url': '',
        'message': '',
        'code': ''
    }

    if 'kakao' in p.findall(url):
        service = 'kakao'
        access_key: str = api_key['apiKey']
        headers: dict = {
            'Authorization': f'KakaoAK {access_key}'
        }
    elif 'naveropenapi' in p.findall(url):
        service = 'naver'
        client_id: str = api_key['clientId']
        client_secret: str = api_key['clientSecret']
        headers: dict = {
            'X-NCP-APIGW-API-KEY-ID': client_id,
            'X-NCP-APIGW-API-KEY': client_secret
        }

    try:
        param = urlencode({'query': '경기 성남시 분당구 야탑동'})
        req = Request(
            url=url+f'?{param}',
            headers=headers
        )
        with urlopen(req) as response:
            result['url'] = response.url
            result['message'] = 'OK'
            result['code'] = response.status
    except HTTPError as error:
        result['url'] = response.url
        result['message'] = error.reason
        result['code'] = error.code
    except URLError as error:
        result['url'] = response.url
        result['message'] = error.reason
        result['code'] = error.errno

    return result


class APIKeyLoader:  # API Key Check and Return
    def __init__(self, file: str) -> None:
        self.file: str = f'{file}.json'
        self.api_key: dict = {}
        self.key_status: bool = False
        self.__api_key_loader()

    def __api_key_loader(self) -> None:
        BASEDIR: str = Path(__file__).resolve().parent.parent.parent

        # API Key File Generation
        if self.file == '.json':
            raise FileNotFoundError("Please input service name")
        if self.file not in os.listdir(f'{BASEDIR}/secure'):
            raise ValueError(
                f"Your '{self.file}' is not found, please make '{self.file}' and input your api access key.")

        # Key File Load
        json_file = open(f'secure/{self.file}', 'r')
        self.api_key = dict(json.loads(json_file.read()))
        json_file.close()

        # Key Data Check
        if self.file == 'kakao.json':
            if bool(self.api_key['apiKey']) is True:
                self.key_status = True
        if self.file == 'naver.json':
            if bool(self.api_key['clientId']) is True:
                if bool(self.api_key['clientSecret']) is True:
                    self.key_status = True

    def load(self) -> dict:
        if self.key_status is False:
            raise ValueError(f'Api key isn`t found in {self.file}')
        return self.api_key


if __name__ == '__main__':
    pass
