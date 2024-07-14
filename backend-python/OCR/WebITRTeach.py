#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#
# 公式识别 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/words/formula-discern/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
#

import requests
import datetime
import hashlib
import base64
import hmac
import json
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, Blueprint
from werkzeug.utils import secure_filename
import os

bp11 = Blueprint('blueprint11', __name__)

class get_result(object):
    def __init__(self, host):
        # 应用ID（到控制台获取）
        self.APPID = "560e7cbc"
        # 接口APISercet（到控制台公式识别服务页面获取）
        self.Secret = "ODYwMDJiMDVkYmNiZmI1MTFjZjE3Nzhm"
        # 接口APIKey（到控制台公式识别服务页面获取）
        self.APIKey = "2fece4d84ef307003b8589a81acfec6d"

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
        # self.AudioPath = "itr/01.png"
        self.BusinessArgs = {
            "ent": "teach-photo-print",
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

    def call_url(self):
        respData = ''
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
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/words/formula-discern/API.html")
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                print(respData)
                # 以下仅用于调试
                code = str(respData["code"])
                if code != '0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")
        return respData


@bp11.route('/latex', methods=['POST'])
def ocr_latex():
    if 'img' not in request.files:
        return "没有文件部分", 400
    file = request.files['img']

    if file.filename == '':
        return "没有选择文件", 400

    if file:
        # 为文件名增加安全性
        # filename = secure_filename(file.filename)
        # 保存文件到本地，这里设置为 'latex.png'
        file.save(os.path.join('OCR', 'latex.png'))


    host = "rest-api.xfyun.cn"
    # 初始化类
    gClass = get_result(host)
    gClass.AudioPath = "latex.png"

    res = gClass.call_url()
    json_str = json.dumps(res, indent=4)
    # print(json_str)
    res_str = ''
    for i in res['data']['region']:
        res_str += str(i['recog']['content'])
    # res = res['data']['region'][0]['recog']['content']
    # print(r'{}'.format(res_str))
    res_str = res_str.replace('ifly-latex-begin', '')
    res_str = res_str.replace('ifly-latex-end', '')
    res_str = res_str.replace(' _ ', '_')

    print(res_str)
    return jsonify({'formula': res_str}), 200
# if __name__ == '__main__':
    # res_format = res_str.replace('\\','\\\\')

    # ax = plt.subplot(111)
    # ax.text(0.1, 0.8, r"$\int_a^b f(x)\mathrm{d}x$", fontsize=30, color="red")
    # ax.text(0.1, 0.3, r"${}$".format(res), fontsize=30)
    # plt.show()
    # print(res_str)  # 格式化结果
