#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tempfile
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from flask import Blueprint

bp2 = Blueprint('blueprint2', __name__)

# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)  # 允许跨域请求

appid = "68e27ab8"
apisecret = "ZWJmMDYyNDlhNDBmNzY4MjlhOTE1ODY1"
apikey = "6ffc41e181499621ed45cedb31c3d3e3"
file_path = '###.png'

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


class universalOcr(object):
    def __init__(self):
        self.appid = appid
        self.apikey = apikey
        self.apisecret = apisecret
        self.url = 'http://api.xf-yun.com/v1/private/hh_ocr_recognize_doc'


    def parse_url(self,requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u

    def get_body(self, file_path):
        # 将payload中数据替换成实际能力内容，参考不同能力接口文档请求数据中payload
        file = open(file_path, 'rb')
        buf = file.read()
        body = {
            "header": {
                "app_id": self.appid,
                "status": 3
            },
            "parameter": {
                "hh_ocr_recognize_doc": {
                    "recognizeDocumentRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "image": {
                    "encoding": "jpg",
                    "image": str(base64.b64encode(buf), 'utf-8'),
                    "status": 3
                }
            }
        }
        # print(body)
        return body


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = universalOcr.parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # date = "Mon, 22 Aug 2022 03:26:45 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    print("signature:",signature_sha)
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    print("authorization:",authorization)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)



def get_result():
    request_url = assemble_ws_auth_url(universalOcr.url, "POST", universalOcr.apikey, apisecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': 'APPID'}
    print(request_url)
    body = universalOcr.get_body(file_path=file_path)
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    print(response)
    re = response.content.decode('utf8')
    str_result = json.loads(re)
    print("\nresponse-content:", re)
    if str_result.__contains__('header') and str_result['header']['code'] == 0:
        renew_text = str_result['payload']['recognizeDocumentRes']['text']
        # res = str_result['payload']['recognizeDocumentRes']['text']
        # print("\ntext解析结果：", str(base64.b64decode(renew_text), 'utf-8'))

        # 将二进制字符串通过utf-8编码，转换化成str
        res = eval(str(base64.b64decode(renew_text), encoding='utf-8'))
        # print(res['whole_text'],type(res))
        return res['whole_text']

universalOcr = universalOcr()
def ocr_transform2text(filepath):
    global file_path
    file_path = filepath
    # global universalOcr

    return get_result()

@bp2.route('/ocr', methods=['POST'])
def orc_function():
    if 'file' not in request.files:
        return "没有文件部分", 400
    file = request.files['file']
    if file.filename == '':
        return "没有选择文件", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 直接使用 Werkzeug 的 secure_filename 函数生成安全的文件名
        file.save(filename) # 保存文件到默认路径

        # 调用OCR函数
        text = ocr_transform2text(filename)
        os.remove(filename)
        # return text  # 返回转换后的文本
        return jsonify({"text": text}), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'png'}


#图片经过base64编码后大小不超过4M
# if __name__ == "__main__":
#     # 将图片进行ocr转化成文字
#     # print(ocr_transform2text("1.jpg"))
#     app.run(port=5006)
