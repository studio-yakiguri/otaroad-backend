import os
import json
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

# Json Message Generator


def message(error, message) -> dict:
    return


def api_server_check(url: str, api_key: str = '') -> dict:  # API Server Check
    service: str = ''
    auth: str = ''
    p = re.compile('[a-z]+')

    if 'kakao' in p.findall(url):
        service = 'kakao'
        auth = f'KakaoAK {api_key}'
    elif 'naveropenapi' in p.findall(url):
        service = 'naver'
        auth = ''

    result: dict = {
        'service': service,
        'url': '',
        'message': '',
        'code': ''
    }

    param = urlencode({'query': '경기 성남시 분당구 야탑동'})

    try:
        req = Request(
            url=url+f'?{param}',
            headers={
                'Authorization': auth
            }
        )
        with urlopen(req) as response:
            # print(json.loads(response.read()))
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
        self.api_key: str = 'None'
        self.api_key_loader()

    def api_key_loader(self) -> None:
        BASEDIR: str = Path(__file__).resolve().parent.parent.parent

        # API Key Generation
        if self.file not in os.listdir(f'{BASEDIR}/secure'):
            f = open(f'secure/{self.file}', 'w')
            file_data: str = '{\n   "key" : ""\n}'
            f.writelines(file_data)
            f.close()

        # Key File Load & Check
        json_file = open(f'secure/{self.file}', 'r')
        api_key: dict = dict(json.loads(json_file.read()))
        self.api_key = api_key['key']
        json_file.close()
        if bool(api_key) is False:
            print('Please input a valid API key')

    def __repr__(self) -> str:
        return self.api_key


if __name__ == '__main__':
    pass
