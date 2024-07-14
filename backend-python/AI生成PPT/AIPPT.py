# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import time

import requests
from flask import Flask, request, jsonify

# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)  # 允许跨域请求

from flask import Blueprint

bp1 = Blueprint('blueprint1', __name__)

APPId = "560e7cbc"
APISecret = "ODYwMDJiMDVkYmNiZmI1MTFjZjE3Nzhm"

class AIPPT():

    def __init__(self,APPId,APISecret,Text):
        self.APPid = APPId
        self.APISecret = APISecret
        self.text = Text
        self.header = {}


    #获取签名
    def get_signature(self, ts):
        try:
            # 对app_id和时间戳进行MD5加密
            auth = self.md5(self.APPid + str(ts))
            # 使用HMAC-SHA1算法对加密后的字符串进行加密
            return self.hmac_sha1_encrypt(auth,self.APISecret)
        except Exception as e:
            print(e)
            return None

    def hmac_sha1_encrypt(self, encrypt_text, encrypt_key):
        # 使用HMAC-SHA1算法对文本进行加密，并将结果转换为Base64编码
        return base64.b64encode(hmac.new(encrypt_key.encode('utf-8'), encrypt_text.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')

    def md5(self, text):
        # 对文本进行MD5加密，并返回加密后的十六进制字符串
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    #创建PPT生成任务
    def create_task(self):
        url = 'https://zwapi.xfyun.cn/api/aippt/create'
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        body= self.getbody(self.text)

        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type":"application/json; charset=utf-8"
        }
        self.header = headers
        response = requests.request("POST",url=url,data= json.dumps(body),headers=headers).text
        resp = json.loads(response)
        if(0 == resp['code']):
            return resp['data']['sid']
        else:
            print('创建PPT任务成功')
            return None

    #构建请求body体
    def getbody(self,text):
        body = {
            "query":text
        }
        return body
		
		
	#轮询任务进度，返回完整响应信息
    def get_process(self,sid):
        print("sid:" + sid)
        if(None != sid):
            response = requests.request("GET",url=f"https://zwapi.xfyun.cn/api/aippt/progress?sid={sid}",headers=self.header).text
            print(response)
            return response
        else:
            return None



    #获取PPT，以下载连接形式返回
    def get_result(self):

        #创建PPT生成任务
        task_id = self.create_task()
        # PPTurl = ''
        #轮询任务进度
        while(True):
            response = self.get_process(task_id)
            resp = json.loads(response)
            process = resp['data']['process']
            if(process == 100):
                PPTurl = resp['data']['pptUrl']
                break
        return PPTurl

def getURL(text):
    demo = AIPPT(APPId, APISecret, text)
    result = demo.get_result()
    return result

@bp1.route('/ppt', methods=['POST'])
def getPPT():
    # 从请求中获取 PPT 名称
    ppt_name = request.form.get('pptName')
    if not ppt_name:
        return jsonify({'error': 'PPT name is required'}), 400

    # 调用 getURL 函数获取下载链接
    download_url = getURL(ppt_name)

    # 返回下载链接给前端
    return jsonify({'download_url': download_url})

# if __name__ == '__main__':
#     app.run(port=5007)
    #需纠错文本
    # Text="集团客户部2023年工作总结"
    # demo = AIPPT(APPId, APISecret, Text)
    # result = demo.get_result()

    # print("生成的PPT请从此地址获取：\n" + result)



