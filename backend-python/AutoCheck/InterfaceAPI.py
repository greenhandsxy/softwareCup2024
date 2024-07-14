import time
import requests
# 接口服务请求类封装，post方式
class InterfaceAPI(object):
    def __init__(self, url, data):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "User-Agent": "Mozilla/5.0  `(Windows NT 10.0; WOW64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
        self.url = url
        self.data = data
        self.response = self.post()

    # 请求数据
    def post(self):
        try:
            print(self.url)
            response = requests.post(self.url, self.data, headers=self.headers, timeout=20)
            return response
        except Exception as e:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: Connect lost! ")
            return -1