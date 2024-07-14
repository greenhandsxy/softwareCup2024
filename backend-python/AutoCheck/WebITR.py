#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#
# 拍照速算识别 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/words/photo-calculate-recg/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
#

import requests
import datetime
import hashlib
import base64
import hmac
import json
from AutoCheck.opencv_utils import paint


class get_result(object):
    def __init__(self, host, img_path):
        # 应用ID（到控制台获取）
        self.APPID = "893b3e80"
        # 接口APISercet（到控制台拍照速算服务页面获取）
        self.Secret = "OWU1ZTAzYTczZmZiMDFkYzM2NGVkNWJj"
        # 接口APIKey（到控制台拍照速算服务页面获取）
        self.APIKey = "9d949e98dd38c96be3ce960282c0fe39"

        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/itr"
        # 设置url
        # print(host)
        self.url = "https://" + host + self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置测试图片文件
        self.AudioPath = img_path
        self.BusinessArgs = {
            "ent": "math-arith",
            "aue": "raw",
        }

    def imgRead(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        # print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        # print(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        audioData = self.imgRead((self.AudioPath))
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "image": content,
            }
        }
        body = json.dumps(postdata)
        # print(body)
        return body

    def check_and_paint(self, rd, img):
        # 获得批改结果以及题目框的坐标
        res = []
        for i, j in enumerate(rd['data']['ITRResult']['multi_line_info']['imp_line_info']):
            lx = j['imp_line_rect']['left_up_point_x']
            ly = j['imp_line_rect']['left_up_point_y']
            rx = j['imp_line_rect']['right_down_point_x']
            ry = j['imp_line_rect']['right_down_point_y']
            res.append(((lx, ly), (rx, ry), j['total_score']))
        paint(img, res)
        print(len(res), '例如：{}'.format(res[0]))

    def call_url(self):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            print('Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。')
        else:
            code = 0
            body = self.get_body()
            headers = self.init_header(body)
            # print(self.url)
            response = requests.post(self.url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            # print(response.content)
            if status_code != 200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/words/photo-calculate-recg/API.html")
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                print(respData)
                print(json.dumps(respData, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
                print('Audiopath:',self.AudioPath)
                self.check_and_paint(respData, self.AudioPath)
                # 以下仅用于调试
                code = str(respData["code"])
                if code != '0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")

def func_cal(filename):
    ##示例:  host="rest-api.xfyun.cn"域名形式
    host = "rest-api.xfyun.cn"
    # 初始化类
    gClass = get_result(host, filename)
    gClass.call_url()

