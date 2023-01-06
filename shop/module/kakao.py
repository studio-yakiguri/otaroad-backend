# 카카오 georecoder module by DongHyeong Lee

import requests

URL: str = "https://dapi.kakao.com/v2/local/search/address.json"

def connection_test() -> bool:
    status_code = ""
    status_reason = ""
    try:
        req = requests.get(URL)
    except:
        
        