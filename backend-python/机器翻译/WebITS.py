#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# 机器翻译 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/nlp/xftrans/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
#
import requests
import datetime
import hashlib
import base64
import hmac
import json
from flask import Flask, request, jsonify
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)  # 允许跨域请求
from flask import Blueprint

bp4 = Blueprint('blueprint4', __name__)

import os
from dotenv import load_dotenv
load_dotenv()

class get_result(object):
    def __init__(self, mode, str):
        # 应用ID（到控制台获取）
        self.APPID = os.environ["SPARKAI_APP_ID"]
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = os.environ["SPARKAI_API_SECRET"]
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey= os.environ["SPARKAI_API_KEY"]

        host = "itrans.xfyun.cn"
        self.Text = str

        if mode == 0:
            self.BusinessArgs = {
                "from": "en",
                "to": "cn",
            }
        else:
            self.BusinessArgs = {
                "from": "cn",
                "to": "en",
            }

        
        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/its"
        # 设置url
        # print(host)
        self.url="https://"+host+self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置业务参数
        # 语种列表参数值请参照接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html

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
        #print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        #print(authHeader)
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
        content = str(base64.b64encode(self.Text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        #print(body)
        return body

    def call_url(self):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            print('Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。')
        else:
            code = 0
            body=self.get_body()
            headers=self.init_header(body)
            #print(self.url)
            response = requests.post(self.url, data=body, headers=headers,timeout=8)
            status_code = response.status_code
            #print(response.content)
            if status_code!=200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html")
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                # print(respData['data']['result']['trans_result']['dst'])
                # 以下仅用于调试
                code = str(respData["code"])
                if code!='0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")
            return respData['data']['result']['trans_result']['dst']


#封装好的函数，mode是翻译模式（0是英译汉，1是汉译英），str是输入的字符串，最后返回翻译后的字符串
def translate(mode, str):
    gClass = get_result(mode, str)
    print(gClass.call_url())
    return gClass.call_url()


@bp4.route('/translate', methods=['POST'])
def translate_api():
    data = request.json
    mode = data.get('mode')
    text = data.get('str')

    # 验证 mode 和 str 是否存在且有效
    if not isinstance(mode, int) or not isinstance(text, str):
        return jsonify({"error": "Invalid input"}), 400

    # 调用 translate 方法，并获取结果
    result = translate(mode, text)

    # 将结果以 JSON 格式返回给前端
    return jsonify({"result": result})

# if __name__ == '__main__':
#     app.run(port=5004)

    # str = translate(0, 'Multi-camera 3D object detection blossoms in recent years and most of '
    #                    'state-of-the-art methods are built up on the bird’s-eye-view (BEV) representations')

    # print(str)
