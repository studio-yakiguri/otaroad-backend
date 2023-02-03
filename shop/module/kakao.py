# 카카오 georecoder module by DongHyeong Lee

import os
import json
import requests

from util import APIKeyLoader, api_server_check

URL: str = "https://dapi.kakao.com/v2/local/search/address.json"

APIKEY: str = APIKeyLoader('kakao')
server_check: dict = api_server_check(URL, APIKEY)

print(server_check)


def is_valid() -> dict:  # 값이 맞는 지 확인
    return


class Geocoding:
    def __init__(self):
        return


if __name__ == '__main__':
    pass
