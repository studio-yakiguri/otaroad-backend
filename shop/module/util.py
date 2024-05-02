import os
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

# Common path settings
BASEDIR: str = Path(__file__).resolve().parent.parent.parent


# API Server Check
class APIServerCheck:
    def __init__(self, url: str, api_key: dict):

        # api_status directory check
        if 'api_status' not in os.listdir(f'{BASEDIR}'):
            os.makedirs(f'{BASEDIR}/api_status')

        # Setting Variable for API Status Data
        self.URL: str = url
        self.API_KEY: str = api_key
        self.headers: dict = None
        self.service: str = None
        self.file: str = None
        self.now_date = datetime.now()
        self.is_api_work: bool = True
        self.server_status: dict = {
            'service': '',
            'url': '',
            'error_name': '',
            'message': '',
            'code': '',
            'req_time': ''
        }

        # Get Data From service status file
        self.__get_service_name()
        try:
            with open(f'{BASEDIR}/api_status/{self.file}', 'r') as file:
                self.server_status: dict = dict(json.loads(file.read()))
                file.close()
        except FileNotFoundError:
            pass

        # Functions Run
        self.__time_comparison()
        if self.__time_comparison() is False:
            self.__set_header()
            self.__api_test()

    def __time_comparison(self) -> bool:
        result: bool = False

        # file not found
        if self.file not in os.listdir(f'{BASEDIR}/api_status'):
            return result

        # Error Detected
        if bool(self.server_status['error_name']) is True:
            return result

        # Setting Variables
        now: datetime = datetime.now()
        req_time: datetime = datetime.strptime(
            self.server_status['req_time'], '%Y/%m/%d-%H:%M:%S')

        # compare requested time
        time_diff: timedelta = now - req_time
        min_diff: int = int(time_diff.seconds / 60)
        if min_diff < 1:
            result = True

        return result

    def __get_service_name(self) -> None:
        p = re.compile('[a-z]+')
        if 'kakao' in p.findall(self.URL):
            self.service = 'kakao'
        elif 'naveropenapi' in p.findall(self.URL):
            self.service = 'naver'
        self.file: str = f'{self.service}_api_status.json.'
        self.server_status['service'] = self.service

    def __set_header(self) -> None:
        if self.service == 'kakao':
            access_key: str = self.API_KEY['api_key']
            self.headers: dict = {
                'Authorization': f'KakaoAK {access_key}'
            }
        elif self.service == 'naver':
            client_id: str = self.API_KEY['client_id']
            client_secret: str = self.API_KEY['client_secret']
            self.headers: dict = {
                'X-NCP-APIGW-API-KEY-ID': client_id,
                'X-NCP-APIGW-API-KEY': client_secret
            }

    def __api_test(self) -> None:
        param = urlencode({'query': '경기 성남시 분당구 야탑동'})
        req_time: str = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        response = None
        try:
            req = Request(
                url=self.URL+f'?{param}',
                headers=self.headers
            )
            response = urlopen(req)
            self.server_status['url'] = self.URL
            self.server_status['message'] = 'OK'
            self.server_status['code'] = response.status
        except HTTPError as error:
            self.server_status['error_name'] = 'HTTPError'
            self.server_status['url'] = self.URL
            self.server_status['message'] = error.reason
            self.server_status['code'] = error.code
            self.is_api_work = False
        except URLError as error:
            err_reason: list = str(error.reason).split(']')
            err_code: int = int(err_reason[0].replace('[', '').split()[1])
            self.server_status['error_name'] = 'URLError'
            self.server_status['url'] = self.URL
            self.server_status['message'] = err_reason[1].strip()
            self.server_status['code'] = err_code
            self.is_api_work = False
        self.server_status['req_time'] = req_time

        # File Generate
        f = open(f'{BASEDIR}/api_status/{self.file}', 'w')
        f.write(json.dumps(self.server_status, indent=4))

    def status(self) -> bool:
        return self.is_api_work


# API Key Check and Return
class APIKeyLoader:
    def __init__(self, file: str) -> None:
        self.file: str = f'{file}.json'
        self.api_key: dict = {}
        self.key_status: bool = False
        self.__api_key_loader()

    def __api_key_loader(self) -> None:

        # API Key File Generation
        if self.file == '.json':
            raise FileNotFoundError("Please input service name")
        if self.file not in os.listdir(f'{BASEDIR}/.secure'):
            raise ValueError(
                f"Your '{self.file}' is not found, please make '{self.file}' and input your api access key.")

        # Key File Load
        json_file = open(f'.secure/{self.file}', 'r')
        self.api_key = dict(json.loads(json_file.read()))
        json_file.close()

        # Key Data Check
        if self.file == 'kakao.json':
            if bool(self.api_key['api_key']) is True:
                self.key_status = True
        if self.file == 'naver.json':
            if bool(self.api_key['client_id']) is True:
                if bool(self.api_key['client_secret']) is True:
                    self.key_status = True

    def load(self) -> dict:
        if self.key_status is False:
            raise ValueError(f'Api key isn`t found in {self.file}')
        return self.api_key


# print pretty for dict -> Only in Debug
def dict_pretty_print(dict) -> None:
    pretty = json.dumps(dict, indent=4, ensure_ascii=False)
    print(pretty)


# Running Time Check -> Logging, Closers
def running_time():
    pass


# Utility Test (Please remove code after Test)
'''
if __name__ == '__main__':
    URL: str = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    APIKEY: dict = APIKeyLoader('naver').load()
    status = APIServerCheck(URL, APIKEY)
    print(status.status())
'''
